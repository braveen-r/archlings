#!/bin/bash
# Break the keyring by deleting the gnupg directory
rm -rf /etc/pacman.d/gnupg

# Attempting to run pacman -Sy now will fail with signature errors
echo "Fault injected: Keyring wiped."
