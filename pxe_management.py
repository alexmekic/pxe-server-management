import retrieve_info, adv_and_update_menu, sync_images_boot_menu_files, list_images_and_entries
import add_remove_edit_boot_entries, rename_delete_image
import os, re, glob, sys, platform
from zfs_pool import PXE

def main():
    management_ver = "1.9.2"
    if not retrieve_info.zfs_health():
        print("Application terminated due to disk error detected in storage pool")
        sys.exit()
    while True:
        if platform.system() == "FreeBSD":
            print("\nFreeBSD version: " + platform.release())
        #elif platform.system() == "Linux":
        #    linux_os = distro.linux_distribution()
        #    print("\nLinux version: " + linux_os[0] + ' ' + linux_os[1] + ' ' + linux_os[2], end='', flush=True)
        if glob.glob(PXE.zfs_pool + '/tftp/clonezilla/Clonezilla-Live-Version'):
            with open(PXE.zfs_pool + '/tftp/clonezilla/Clonezilla-Live-Version') as f:
                clonezilla_ver = f.readline()
            clonezilla_ver = re.search('clonezilla-live-(.*)-amd64', clonezilla_ver).group(1)
            print("Clonezilla version: " + str(clonezilla_ver), end='', flush=True)
        else:
            print('Clonezilla not installed!')
        ip_addr, netmask_addr = retrieve_info.active_ip()
        print("\nCurrent static IP address: " + ip_addr + " netmask: " + netmask_addr)
        free_space = os.popen("df -lh | grep " + PXE.zfs_pool + " | awk '{print $4}'").read()
        print("Free space available in " + PXE.zfs_pool + ": " + free_space)
        prompt = user_input()
        if prompt == 1:
            add_remove_edit_boot_entries.add_restore_entry()
        elif prompt == 2:
            list_images_and_entries.list_entry()
        elif prompt == 3:
            list_images_and_entries.list_images()
        elif prompt == 4:
            add_remove_edit_boot_entries.set_default_entry()
        elif prompt == 5:
            add_remove_edit_boot_entries.change_attached_restore_image()
        elif prompt == 6:
            rename_delete_image.rename_image_name()
        elif prompt == 7:
            add_remove_edit_boot_entries.revert_menu_change()
        elif prompt == 8:
            add_remove_edit_boot_entries.delete_entry()
        elif prompt == 9:
            rename_delete_image.delete_image()
        elif prompt == 10:
            sync_images_boot_menu_files.sync_menu(ip_addr)
        elif prompt == 11:
            adv_and_update_menu.update_menu(management_ver, clonezilla_ver, platform.release())
        elif prompt == 12:
            adv_and_update_menu.adv_menu(ip_addr, netmask_addr)
        elif prompt == 0:
            sys.exit()
        else:
            print("Invalid Option")
        input("Press Enter to continue...")

def user_input():
    while True:
        options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '0']
        print("PXE Server Management Application v2.0 Beta 3\n")
        print("1: Create new boot entry")
        print("2: List boot entries")
        print("3: List restore images\n")
        print("4: Change default boot entry")
        print("5: Change restore image from boot entry")
        print("6: Rename restore image\n")
        print("7: Revert to previous state of boot entry file")
        print("8: Delete boot entry")
        print("9: Delete restore image\n")
        print("10: Sync images and boot entry to another server\n")
        print("11: Check for updates")
        print("12: Advanced Options\n")
        print("0: Exit to shell\n")
        prompt = (input("> "))
        if prompt == "0":
            sys.exit()
        elif prompt in options:
            return int(prompt)
        else:
            print("Invalid Selection\n")

main()