#!/bin/bash
# Create a fake lock file to simulate an interrupted pacman transaction
touch /var/lib/pacman/db.lck

echo "Fault injected: Stale db.lck file created."
