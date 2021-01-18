import change_server_config
import subprocess, os, shutil, dirsync, fileinput
from zfs_pool import PXE
from pathlib import Path

def mount_network_dir(backup_storage_pool, second_server_ip):
    print("Mounting " + backup_storage_pool + " from " + second_server_ip + "...", end='', flush=True)
    os.mkdir(PXE.zfs_pool + '/nfsmount')
    exit_code = subprocess.call('sudo mount_nfs -o retrycnt=1 ' + second_server_ip + ":/" + backup_storage_pool + " " + PXE.zfs_pool + "/nfsmount", shell=True)
    if exit_code != 0:
        print("failed")
        print("Unable to mount remote network directory")
        os.rmdir(PXE.zfs_pool + '/nfsmount')
        return False
    else:
        print("done")
        return True

#fix this
def copy_entry_file(main_server_ip, second_server_ip, direction):
    try:
        if direction == 'upload':
            print("Uploading boot menu file to " + second_server_ip + "...", end='', flush=True)
            filepath = Path(PXE.zfs_pool + '/nfsmount/boot.ipxe')
            filepath.rename(filepath.with_suffix('.ipxe.bak'))
            shutil.copy2(PXE.zfs_pool + '/tftp/boot.ipxe', PXE.zfs_pool + '/nfsmount/')
            with fileinput.FileInput(PXE.zfs_pool + '/nfsmount/boot.ipxe', inplace=True) as file:
                for line in file:
                    print(line.replace(main_server_ip, second_server_ip), end='')
        elif direction == "download":
            print("Downloading boot menu file from " + second_server_ip + "...", end='', flush=True)
            filepath = Path(PXE.zfs_pool + '/tftp/boot.ipxe')
            filepath.rename(filepath.with_suffix('.ipxe.bak'))
            shutil.copy2(PXE.zfs_pool + '/nfsmount/boot.ipxe', PXE.zfs_pool + '/tftp/')
            with fileinput.FileInput(PXE.zfs_pool + '/tftp/boot.ipxe', inplace=True) as file:
                for line in file:
                    print(line.replace(main_server_ip, second_server_ip), end='')
        print("done")
    except:
        print("failed")

def sync_images():
    try:
        # subprocess.call('find /' + PXE.zfs_pool + '/images -type d -print0 | sudo xargs -0 chmod 0770', shell=True)
        # subprocess.call('find /' + PXE.zfs_pool + '/images -type f -print0 | sudo xargs -0 chmod 0660', shell=True)
        # subprocess.call('find /' + PXE.zfs_pool + '/nfsmount -type d -print0 | sudo xargs -0 chmod 0770', shell=True)
        # subprocess.call('find /' + PXE.zfs_pool + '/nfsmount -type f -print0 | sudo xargs -0 chmod 0660', shell=True)
        print("Syncing images from main to backup...", end='', flush=True)
        dirsync.sync(PXE.zfs_pool + '/images', PXE.zfs_pool + '/nfsmount', 'sync')
        print("done")
        print("Syncing images from backup to main...", end='', flush=True)
        dirsync.sync(PXE.zfs_pool + '/nfsmount', PXE.zfs_pool + '/images', 'sync')
        print("done")
    except:
        print("failed")

def sync_server(main_server_ip, sync_type):
    while True:
        second_server_ip = input("Enter IP address of secondary/backup server (x to exit): ")
        if second_server_ip == "x":
            print("Operation aborted")
            break
        elif change_server_config.is_valid_ipv4_address(second_server_ip):
            print("Checking if " + second_server_ip + " is reachable...")
            ping_response = os.system("ping -c 5 " + second_server_ip)
            if ping_response == 0:
                print("Success")
                while True:
                    backup_storage_pool = input("Enter full path of storage pool from backup server (0 to exit): ")
                    if backup_storage_pool == "0":
                        print("Operation aborted")
                        break
                    else:
                        if mount_network_dir(backup_storage_pool, second_server_ip):
                            if sync_type == "1":
                                sync_images()
                            elif sync_type == "2":
                                copy_entry_file(main_server_ip, second_server_ip, "upload")
                            elif sync_type == "3":
                                copy_entry_file(main_server_ip, second_server_ip, "download")
                            print("Unmounting...", end='', flush=True)
                            subprocess.call("sudo umount " + PXE.zfs_pool + "/nfsmount", shell=True)
                            os.rmdir(PXE.zfs_pool + '/nfsmount')
                            print("done")
                            break
                        else:
                            continue
                break
            else:
                print("Server is not reachable. Check connection and network settings")
        else:
            print("Invalid IP address")

def sync_menu(main_server_ip):
    while True:
        options = ['1', '2', '3', '0']
        print("PXE Server Syncing Menu\n")
        print("1: Sync images with another server")
        print("2: Upload/backup boot menu file to another server")
        print("3: Download boot menu file from another server")
        print()
        sync_prompt = input("> ")
        if sync_prompt == '0':
            break
        elif sync_prompt in options:
            sync_server(main_server_ip, sync_prompt)
        else:
            print("Invalid Option") 
