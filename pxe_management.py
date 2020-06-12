import retrieve_info, adv_and_update_menu, sync_images_boot_menu_files, list_images_and_entries
import add_remove_edit_boot_entries, rename_delete_image
import os, re, glob, sys, platform

def main():
    if not retrieve_info.zfs_health():
        sys.exit()
    while True:
        if platform.system() == "FreeBSD":
            print("\nFreeBSD version: " + platform.release())
        #elif platform.system() == "Linux":
        #    linux_os = distro.linux_distribution()
        #    print("\nLinux version: " + linux_os[0] + ' ' + linux_os[1] + ' ' + linux_os[2], end='', flush=True)
        if glob.glob('/pxe/tftp/clonezilla/Clonezilla-Live-Version'):
            with open('/pxe/tftp/clonezilla/Clonezilla-Live-Version') as f:
                clonezilla_ver = f.readline()
            clonezilla_ver = re.search('clonezilla-live-(.*)-amd64', clonezilla_ver).group(1)
            print("Clonezilla version: " + str(clonezilla_ver), end='', flush=True)
        else:
            print('Clonezilla not installed!')
        ip_addr, netmask_addr = retrieve_info.active_ip()
        print("\nCurrent static IP address: " + ip_addr + " netmask: " + netmask_addr)
        free_space = os.popen("df -lh | grep /pxe | awk '{print $4}'").read()
        print("Free space available in /pxe: " + free_space)
        prompt = user_input()
        if prompt == 1:
            list_images_and_entries.list_entry()
        elif prompt == 2:
            list_images_and_entries.list_images()
        elif prompt == 3:
            add_remove_edit_boot_entries.add_restore_entry()
        elif prompt == 4:
            add_remove_edit_boot_entries.change_attached_restore_image()
        elif prompt == 5:
            add_remove_edit_boot_entries.set_default_entry()
        elif prompt == 6:
            rename_delete_image.rename_image_name()
        elif prompt == 7:
            add_remove_edit_boot_entries.revert_menu_change()
        elif prompt == 8:
            add_remove_edit_boot_entries.delete_entry()
        elif prompt == 9:
            rename_delete_image.delete_image()
        elif prompt == 10:
            sync_images_boot_menu_files.sync_server(ip_addr)
        elif prompt == 11:
            adv_and_update_menu.update_menu(clonezilla_ver, platform.release())
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
        print("PXE Server Management v1.3\n")
        print("1: List current entries and restore images attached")
        print("2: List restore images in server")
        print("3: Add New restore entry\n")
        print("4: Change Attached Restore Image in entry")
        print("5: Change default entry")
        print("6: Rename restore image in server\n")
        print("7: Revert change in menu file to previous state")
        print("8: Delete entry")
        print("9: Delete image\n")
        print("10: Sync restore images and menu file to another server\n")
        print("11: Check Clonezilla and FreeBSD updates")
        print("12: Enter Advanced Menu\n")
        print("0: Exit to shell\n")
        prompt = (input("LOAD: "))
        if prompt == "0":
            sys.exit()
        elif prompt in options:
            return int(prompt)
        else:
            print("Invalid Selection\n")

if __name__ == "__main__":
    main()