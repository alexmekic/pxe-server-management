# Manage your Deployed Clonezilla PXE Server

Easily manage Clonezilla iPXE boot menu entries and operating system restore images backed up written in Python for restoring images to client computers over network

## Features
### List all restore images and boot entries

- Show a list of all restore images stored in the ZFS storage pool

- Show all bootable Clonezilla and OS entries from `boot.ipxe` available to the client computer when it boots over network to the PXE server

- Boot entry list shows entry ID, description and attached restore image that will be used to restore the associated restore image to the client computer automatically

### Add, edit and remove boot entries and images

- Add a boot entry in the iPXE boot menu file by prompting user for the restore image stored in /pxe/images, entry ID and description to the `boot.ipxe` with default settings:

- Edit a boot entry to change the restore image attached and change the default boot entry ID with timeout that client computer will boot off automatically

- Remove a boot entry from the boot menu iPXE file and revert the most recent change of the boot menu file in event of accidental add/remove/edit

- Easily rename and delete a restore image

### Update Clonezilla Live

- Checks for the latest version of Clonezilla Live, downloads and installs at user's request

- Backs up the current version of Clonezilla Live before installing the latest version

- Revert Clonezilla to the previous version in event of a corrupted update of Clonezilla

### Update FreeBSD packages and upgrade FreeBSD OS release

- Checks for updates on FreeBSD packages installed on the server and installs the latest

- Checks for minor or major upgrades available for FreeBSD and upgrades to the latest

  - NOTE: Script currently requires user accept or decline OS configuration is reasonable and type in a couple commands after first reboot via the command `sudo freebsd-update install`.

### Sync boot entry file and images to another server

- Checks the desired backup server is reachable via `ping`

- Copies the latest version of the boot entry file and restore images from the source server to the backup, and vice versa for restore images only

## Advanced Features

- Change static IP address
  - Updates all DHCP, and TFTP configuration files that depends on the static IP
- Change DHCP server IP address range
- Change admin account password
- Shutdown and reboot the server
- Check health of ZFS storage pool

## Release History

- 1.0
  - Initial release
  - 1.0.1
    - Fixed missing 'wget' module for downloading updated version of Clonezilla
- 1.1
  - Added password change prompt for Samba when change admin password option is selected
  - Reorganized main menu selection options
- 1.2
  - Added feature to check ZFS storage pool health before launch of application
  - Rearranged main menu options

- 2.0 (currently in beta)
  - Edited output for list of images in tabular format and extended image name length printed on screen
  - Included size of images when listed
  - Shifted location of new image restore entries down by 1 to accomodate new entry for booting Clonezilla Live
  - Removed index number of restore entries printed on screen when listing
  - Renamed menu entries for clarity
  - Merged `clonezilla_updater` and `freebsd_updater` to `pxe_updater`
  - Removed need for `chown` user permission changes during syncing
  - Added update option for PXE Management Application
