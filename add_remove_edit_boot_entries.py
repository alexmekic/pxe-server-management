import list_images_and_entries, retrieve_info
import os, glob, shutil, fileinput, re, sys

def add_restore_entry():
    image_list = list_images_and_entries.list_images()
    while True:
        new_image_entry = input("Enter image index (x to exit): ")
        try:
            if new_image_entry == "x":
                print("Operation aborted")
                break
            elif check_image_in_use(image_list[int(new_image_entry)]):
                print("Restore image " + image_list[int(new_image_entry)] + " already in use by another restore entry")
            else:
                new_entry_id = input("Enter entry ID: ")
                new_entry_desc = input("Enter Restore description name: ")
                restore_type, partition_list = retrieve_info.get_image_partitions(image_list[int(new_image_entry)])
                nfs_ip = retrieve_info.active_ip()[0]
                cz_root = '{cz_root}'
                entry1 = f"item {new_entry_id} Restore {new_entry_desc}\n"
                entry2 = f""":{new_entry_id}
set cz_root nfs://{nfs_ip}/pxe/tftp/clonezilla/live
kernel ${cz_root}/vmlinuz initrd=initrd.img boot=live username=user union=overlay config components noswap edd=on nomodeset nodmraid locales=en_US.UTF-8 keyboard-layouts=NONE ocs_live_run="ocs-live-general" ocs_live_extra_param="" ocs_live_batch=no net.ifnames=0 nosplash noprompt ip=frommedia netboot=nfs nfsroot={nfs_ip}:/pxe/tftp/clonezilla ocs_prerun1="mount -t nfs {nfs_ip}:/pxe/images /home/partimag -o noatime,nodiratime," oscprerun2="sleep 10" ocs_live_run="/usr/sbin/ocs-sr -g auto -e2 -scr -nogui -j2 -p reboot {restore_type} {image_list[int(new_image_entry)]} {partition_list}"
initrd ${cz_root}/initrd.img
imgstat
boot\n"""
                shutil.copy2('/pxe/tftp/boot.ipxe', '/pxe/tftp/boot.ipxe.bak')
                with open('/pxe/tftp/boot.ipxe', 'r') as f1:
                    t1 = f1.readlines()
                t1.insert(7, entry1)
                t1.append(entry2)
                with open('/pxe/tftp/boot.ipxe', 'w') as f2:
                    f2.writelines(t1)
                print("New Restore entry for " + new_entry_desc + " added successfully")
        except (ValueError, IndexError):
            print("Invalid image selection")
       
def change_attached_restore_image():
    matched_images = []
    while True:
        entry_id, entry_items, attached_image = list_images_and_entries.list_entry()
        entry_id_edit = input("Enter Entry ID to change attached restore image (x to exit): ")
        if entry_id_edit == "x":
            print("Operation aborted")
            break
        elif entry_id_edit in entry_id:
            old_index = entry_id.index(entry_id_edit)
            image_list = list_images_and_entries.list_images()
            new_attached_image = input("Enter restore image index: ")
            try:
                if check_image_in_use(image_list[int(new_attached_image)]):
                    print("Restore image " + image_list[int(new_attached_image)] + " already attached to another restore entry")
                else:
                    with fileinput.FileInput('/pxe/tftp/boot.ipxe', inplace=True, backup='.bak') as file:
                        for line in file:
                            if line.startswith('kernel'):
                                print(line.replace(attached_image[int(old_index)], image_list[int(new_attached_image)]), end='')
                            else:
                                print(line.strip("\n"))
                    print("Entry " + entry_items[int(old_index)] + " attached restore image set to " + image_list[int(new_attached_image)])
                    break
            except (ValueError, IndexError):
                print("Invalid image selection")
        else:
            print("Entry ID not found")

def delete_entry():
    entry_id, entry_name, attached_image = list_images_and_entries.list_entry()
    while True:
        entry_delete = input("Enter Entry ID of Image to delete (0 to exit): ")
        if entry_delete == '0':
            print("Operation aborted")
            break
        elif entry_delete in entry_id:
            index = entry_id.index(entry_delete)
            delete_confirm = input("Warning: Are you sure you want to delete " + entry_name[int(index)] + "? (y/n):")
            if delete_confirm == 'y':
                shutil.copy2('/pxe/tftp/boot.ipxe', '/pxe/tftp/boot.ipxe.bak')
                copying = True
                with open('/pxe/tftp/boot.ipxe.bak', 'r') as inf, open('/pxe/tftp/boot.ipxe', 'w') as outf:
                    for line in inf:
                        if copying:
                            if line.startswith(':') and entry_delete in line:
                                copying = False
                            elif not line.startswith('item ' + entry_delete):
                                outf.write(line)
                        elif line.startswith('boot'):
                            copying = True
                print("Entry " + entry_name[index] + " deleted")
                break
            else:
                print("Invalid Entry ID")

def revert_menu_change():
    if glob.glob('/pxe/tftp/boot.ipxe.bak'):
        while True:
            revert_option = input("Are you sure you want to revert to the previous state? (y/n): ")
            if revert_option == 'y':
                os.remove('/pxe/tftp/boot.ipxe')
                shutil.copy2('/pxe/tftp/boot.ipxe.bak', '/pxe/tftp/boot.ipxe')
                print("Boot menu file reverted successfully")
                break
            elif revert_option == 'n':
                print("Operation aborted")
                break
            else:
                print("Invalid option")
    else:
        print('No backup menu file found')

def set_default_entry():
    entry_id, entry_name, attached_image = list_images_and_entries.list_entry()
    while True:
        new_default = input("Enter Entry ID of Image to set as default (0 to exit): ")
        if new_default == '0':
            print("Operation aborted")
            break
        elif new_default in entry_id:
            index = entry_id.index(new_default)
            while True:
                timeout = input("Enter time in seconds (or 0 to disable timeout): ")
                option = '{option}'
                if timeout == '0':
                    new_default_command = f"choose --default {new_default} option && goto ${option}\n"
                    break
                else:
                    try:
                        timeout = int(timeout)
                        new_default_command = f"choose --default {new_default} --timeout {timeout}000 option && goto ${option}\n"
                        break
                    except ValueError:
                        print("Timeout value not valid")
            shutil.copy2('/pxe/tftp/boot.ipxe', '/pxe/tftp/boot.ipxe.bak')
            for line in fileinput.input('/pxe/tftp/boot.ipxe', inplace=True, backup='.bak'):
                if line.strip().startswith('choose --default'):
                    line = new_default_command
                sys.stdout.write(line)
            print("New default entry set to " + entry_name[index])
            break
        else:
            print("Entry ID not found in menu file")

def check_image_in_use(image):
    with open('/pxe/tftp/boot.ipxe', 'r') as pxe_search:
        for line in pxe_search:
            if line.startswith('kernel'):
                image_scan = re.search(r'\b'+image+'\s', line)
                if image_scan:
                    return True
    return False