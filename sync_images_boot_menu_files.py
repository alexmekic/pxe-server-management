import change_server_config, subprocess, os, shutil, dirsync, fileinput

def sync_server(main_server_ip):
    while True:
        second_server_ip = input("Enter IP address of secondary/backup server (x to exit): ")
        if second_server_ip == "x":
            print("Operation aborted")
            break
        elif change_server_config.is_valid_ipv4_address(second_server_ip):
            print("Checking if " + second_server_ip + " is reachable...")
            ping_response = os.system("ping -c 5 " + second_server_ip)
            if ping_response == 0:
                print("Server is reachable. Syncing images and boot menu file...")
                subprocess.call('sudo mkdir /pxe/nfsmount', shell=True)
                print("Attempting to mount boot menu directory from " + second_server_ip + "...", end='', flush=True)
                exit_code = subprocess.call('sudo mount_nfs -o retrycnt=1 ' + second_server_ip + ":/pxe/tftp /pxe/nfsmount", shell=True)
                if exit_code != 0:
                    print("failed")
                    print("Mounting from " + second_server_ip + " for updating boot menu file failed.")
                else:
                    print("done")
                    print("Updating boot menu file...", end='', flush=True)
                    shutil.copy2("/pxe/nfsmount/boot.ipxe", "/pxe/nfsmount/boot.ipxe.bak")
                    os.remove("/pxe/nfsmount/boot.ipxe")
                    shutil.copy2("/pxe/tftp/boot.ipxe", "/pxe/nfsmount/boot.ipxe")
                    print("done")
                with fileinput.FileInput('/pxe/nfsmount/boot.ipxe', inplace=True) as file:
                    for line in file:
                        print(line.replace(main_server_ip, second_server_ip), end='')
                subprocess.call("sudo umount /pxe/nfsmount", shell=True)
                print("Attempting to mount images directory from " + second_server_ip + "...", end='', flush=True)
                exit_code = subprocess.call('sudo mount_nfs -o retrycnt=1 ' + second_server_ip + ":/pxe/images /pxe/nfsmount", shell=True)
                if exit_code != 0:
                    print("failed")
                    print("Mounting from " + second_server_ip + " for updating images failed.")
                else:
                    print("done")
                    print("Syncing images from main to backup...", end='', flush=True)
                    subprocess.call('sudo chown -R admin:admin /pxe/images', shell=True)
                    subprocess.call('find /pxe/images -type d -print0 | sudo xargs -0 chmod 0755', shell=True)
                    subprocess.call('find /pxe/images -type f -print0 | sudo xargs -0 chmod 0644', shell=True)
                    dirsync.sync('/pxe/images', '/pxe/nfsmount', 'sync')
                    print("done")
                    print("Syncing images from backup to main...", end='', flush=True)
                    dirsync.sync('/pxe/nfsmount', '/pxe/images', 'sync')
                    subprocess.call('sudo chown -R admin:admin /pxe/images', shell=True)
                    subprocess.call('find /pxe/images -type d -print0 | sudo xargs -0 chmod 0755', shell=True)
                    subprocess.call('find /pxe/images -type f -print0 | sudo xargs -0 chmod 0644', shell=True)
                    subprocess.call('sudo chmod 753 /pxe/images', shell=True)
                    subprocess.call('sudo umount /pxe/nfsmount', shell=True)
                    subprocess.call('sudo rm -r /pxe/nfsmount', shell=True)
                    print("done")
                break
            else:
                print("Server is not reachable. Check connection and network settings")
        else:
            print("Invalid IP address")