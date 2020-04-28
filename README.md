# Clonezilla iPXE Server Management Application

Easily manage Clonezilla iPXE boot menu entries and operating system restore images backed up written in Python for restoring images to client computers over network

## Features
### List all restore images and boot entries

- Show a list of all restore images stored in `/pxe/images`:

- Show all boot entries from `/pxe/tftp/boot.ipxe` available to the client computer when it boots over network to the PXE server:

- Boot entry list shows entry ID, description and attached restore image that will be used to restore the associated restore image to the client computer automatically

### Add, edit and remove boot entries and images

- Add a boot entry in the iPXE boot menu file by prompting user for the restore image stored in /pxe/images, entry ID and description to the `/pxe/tftp/boot.ipxe` with default settings:

- Edit a boot entry to change the restore image attached and change the default boot entry ID with timeout that client computer will boot off automatically

- Remove a boot entry from the boot menu iPXE file and revert the most recent change of the boot menu file in event of accidental add/remove/edit

- Easily rename and delete a restore image

### Update and revert version of Clonezilla

- Update version of Clonezilla installed under `/pxe/tftp/clonezilla` to the latest version

- Revert Clonezilla to the previous version in event of a corrupted update of Clonezilla

### Update FreeBSD

- Update FreeBSD to the latest version

  - NOTE: Script currently requires user accept or decline OS configuration is reasonable and type in a couple commands after first reboot via the command `sudo freebsd-update install`.

### Sync boot entry file and images to another server

- Copy the `/pxe/tftp/boot.ipxe` file from the main server to the backup server and sync all restore images between both servers

## Advanced Features

- Change static IP address
  - Updates all configuration files that depends on the static IP
- Change DHCP server IP address range
- Change admin account password
- Reset permissions on /pxe/images
  - Used for accessing images from Windows
- Shutdown and reboot the server
- Check health of ZFS storage pool

## Requirements

- FreeBSD 12.1 or later
- 2nd hard drive or SSD with `/pxe` mounted on startup from `/etc/fstab` formatted as UFS or ZFS
- `postinstall.sh` executed from `clonezillaserver-deployment` project with static IP, DHCP server, admin account creation and password, Samba, iPXE and Clonezilla configured

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
