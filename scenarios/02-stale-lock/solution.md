# Solution: Stale Lock File

When pacman is interrupted abruptly (e.g., power loss or forced exit), it leaves behind a lock file to prevent database corruption. 

If you are absolutely sure no other pacman instance is running in the background, you can safely remove the lock file:

```bash
rm /var/lib/pacman/db.lck
pacman -Sy

