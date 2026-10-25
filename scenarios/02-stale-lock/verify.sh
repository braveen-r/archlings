#!/bin/bash
# Ensure the lock file is gone and pacman can run
if [ -f /var/lib/pacman/db.lck ]; then
    echo "❌ The db.lck file is still present. Keep trying!"
    exit 1
fi

if pacman -Sy --noconfirm > /dev/null 2>&1; then
    echo "✅ Lock verified removed! pacman is working again."
    exit 0
else
    echo "❌ pacman failed for another reason. Did you break something else?"
    exit 1
fi
