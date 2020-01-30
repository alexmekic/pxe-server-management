import clonezilla_updater, freebsd_updater
import change_server_config
import subprocess

def update_menu(clonezilla_ver, freebsd_version):
    while True:
        print("\nPXE Server Update Menu\n")
        print("1: Check updates for Clonezilla")
        print("2: Revert previous Clonezilla version")
        print("3: Check patch and package updates for FreeBSD (Reboot may be required)")
        print("4: Check minor or major updates for FreeBSD (Reboot will be required)")
        print("0: Exit back to Main Menu\n")
        update_prompt = input("LOAD: ")
        if update_prompt == "1":
            clonezilla_updater.check_clonezilla_update(clonezilla_ver)
        elif update_prompt == "2":
            clonezilla_updater.revert_clonezilla()
        elif update_prompt == "3":
            freebsd_updater.check_package_patch_updates()
        elif update_prompt == "4":
            freebsd_updater.check_freebsd_updates(freebsd_version.split('-')[0])
        elif update_prompt == "0":
            break
        else:
            print("Invalid Option")

def adv_menu(ip_addr, netmask_addr):
    while True:
        print("\nPXE Advanced Menu\n")
        print("1: Change static IP address")
        print("2: Change DHCP IP address range")
        print("3: Change admin account password")
        print("4: Reset permissions on /pxe/images")
        print("5: Reboot Server")
        print("6: Shutdown Server")
        print("0: Exit back to Main Menu\n")
        adv_prompt = input("LOAD: ")
        if adv_prompt == "1":
            change_server_config.change_ip_address(ip_addr, netmask_addr)
        elif adv_prompt == "2":
            change_server_config.change_dhcp_range()
        elif adv_prompt == "3":
            subprocess.call('passwd', shell=True)
        elif adv_prompt == "4":
            subprocess.call('sudo chown -R admin:admin /pxe/images', shell=True)
            subprocess.call('find /pxe/images -type d -print0 | sudo xargs -0 chmod 0755', shell=True)
            subprocess.call('find /pxe/images -type f -print0 | sudo xargs -0 chmod 0644', shell=True)
            subprocess.call('sudo chmod 753 /pxe/images', shell=True)
            print("Permissions on /pxe/images reset successfully")
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