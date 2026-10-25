#!/bin/bash
# We must verify that pacman can actually validate and install a NEW package.
# We use 'nano' because it is not pre-installed in the base container.
if pacman -S --noconfirm nano > /dev/null 2>&1; then
    echo "✅ Keyring verified! pacman is safely installing packages again."
    exit 0
else
    echo "❌ Signature error still present. Keep trying!"
    exit 1
fi
