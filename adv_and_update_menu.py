import pxe_updater, change_server_config
import subprocess
from zfs_pool import PXE

def update_menu(management_ver, clonezilla_ver, freebsd_version):
    while True:
        print("\nPXE Server Update Menu\n")
        print("1: Check updates for PXE Management Application")
        print("2: Check updates for Clonezilla")
        # print("3: Revert to previous version of PXE Management Application")
        print("3: Revert to previous version of Clonezilla")
        print("4: Check patch and package updates (Reboot recommended)")
        print("5: Check for OS upgrades (Reboot required)")
        print("0: Exit back to Main Menu\n")
        update_prompt = input("> ")
        if update_prompt == "1":
            pxe_updater.check_management_update(management_ver)
        elif update_prompt == "2":
            pxe_updater.check_clonezilla_update(clonezilla_ver)
        # elif update_prompt == "3":
        #     pxe_updater.revert_pxe_management()
        elif update_prompt == "3":
            pxe_updater.revert_clonezilla()
        elif update_prompt == "4":
            pxe_updater.check_package_patch_updates()
        elif update_prompt == "5":
            pxe_updater.check_freebsd_updates(freebsd_version.split('-')[0])
        elif update_prompt == "0":
            break
        else:
            print("Invalid Option")

def adv_menu(ip_addr, netmask_addr):
    while True:
        print("\nPXE Advanced Menu\n")
        print("1: Change static IP address")
        print("2: Change DHCP IP address range")
        #print("3: Flush DHCP Cache")
        print("3: Change admin account password")
        print("4: Reset permissions")
        print("5: Reboot Server")
        print("6: Shutdown Server")
        print("0: Exit back to Main Menu\n")
        adv_prompt = input("> ")
        if adv_prompt == "1":
            change_server_config.change_ip_address(ip_addr, netmask_addr)
        elif adv_prompt == "2":
            change_server_config.change_dhcp_range()
        elif adv_prompt == "3":
            print("Enter new admin login account password.")
            subprocess.call('passwd', shell=True)
            print("Enter new admin Samba password for access of files on server from Windows.")
            subprocess.call('smbpasswd', shell=True)
        elif adv_prompt == "4":
            subprocess.call('sudo chmod 770 /' + PXE.zfs_pool + '/images', shell=True)
            print("Permissions reset successfully")
        elif adv_prompt == "5":
            print("Rebooting server...")
            subprocess.call('sudo reboot', shell=True)
        elif adv_prompt == "6":
            print("Shutting Down server...")
            subprocess.call('sudo poweroff', shell=True)
        elif adv_prompt == "0":
            break
        else:
            print("Invalid Option") 