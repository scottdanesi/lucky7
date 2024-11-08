#!/bin/sh

handle_kill() {
    echo "Caught SIGTERM signal. Exiting..."
    exit 0
}

find_emmc() {
    # Find the eMMC device with the largest size (at least 28GB)
    min_size_gb=28
    # Store the result here
    emmc_device_path=""
    # Iterate through the devices using lsblk
    while read -r line; do
        # Extract device name and size columns
        device_name=$(echo "$line" | awk '{print $1}')
        device_size_raw=$(echo "$line" | awk '{print $2}')
        device_size_gb=$(echo "scale=2; $(echo "$device_size_raw" | sed 's/[B|M|G]$//') / 1024 / 1024 / 1024" | bc -l)

        # Check if the device is an eMMC device and its size is at least 20GB
        if [[ "$device_name" =~ "mmcblk" ]]; then
            # Remove the "G" character and compare sizes
            if (( $(echo "$device_size_gb >= $min_size_gb" | bc -l) )); then
                emmc_device_path="/dev/$device_name"
                break
            fi
        fi
    done <<< "$(lsblk -o NAME,SIZE -nrb)"
    echo "$emmc_device_path"
}

# Mount our EFI var filesystem
mount -t efivarfs none /sys/firmware/efi/efivars

if grep -q "nxpmethod=INSTALLER" /proc/cmdline; then
    SOURCE_DEVICE=/dev/sda3
    TARGET_DEVICE=$(find_emmc)
    clear
    echo "**********************************************************"
    echo "**********************************************************"
    echo "**********************************************************"
    echo "**********************************************************"
    echo "Installing pinball operating system to eMMC..."
    echo "**********************************************************"
    echo ""
    echo ""
    echo ""
    echo "    SOURCE DEVICE: ${SOURCE_DEVICE}"
    echo "    TARGET DEVICE: ${TARGET_DEVICE}"
    mount -o remount,rw /
    mkdir /installer
    mount ${SOURCE_DEVICE} /installer 2>/dev/null
    # If we can find the installer payload, then install the operating system
    if [ -f /installer/rootfs.img.gz ]; then
        echo "Found installer payload. Installing operating system..."
        gzip -dc /installer/rootfs.img.gz | dd of=${TARGET_DEVICE} bs=1M status=progress
        echo "Operating system installed."
    else
        echo "Installer payload not found. Exiting."
        exit 1
    fi
    sync

    echo "Creating EFI boot entries..."
    # Set the appropriate EFI boot entry
    efibootmgr -c -d ${TARGET_DEVICE} -p 1 -L "Pinball OS" -l '\EFI\BOOT\BOOTX64.EFI'

    mount -o remount,ro /
    echo ""
    echo ""
    echo "*** Installation completed. Power off, remove USB drive, and power on. ***"
    #while :; do sleep 1; done
    #reboot
else
    # Alsa mixer, set master volume to 100%
    amixer sset Master 100%
    clear
    game_device=$(blkid -U 44c6de08-a268-46db-ab9e-176d3c70fde2)
    data_device=$(blkid -U 44c6de08-a268-46db-ab9e-176d3c70fde3)
    mount $game_device /game
    mount $data_device /data
    echo "Starting game..."
    cd /game
    trap handle_kill SIGTERM SIGINT
    python3 game.py >> "/data/gamelog-$(date '+%Y-%m-%d').txt" 2>&1
fi
