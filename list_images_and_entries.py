import os, subprocess
from itertools import islice
from netifaces import interfaces, ifaddresses, AF_INET

def list_images():
    image_list = []
    print('{:<7s}{:<30s}{}'.format("Index:", "Images:", "Size:"))
    for index, images in enumerate(os.listdir("/pxe/images"), start=0):
        image_list.append(images)
        imagesize = subprocess.check_output(['du','-sh', "/pxe/images/" + images]).split()[0].decode('utf-8')
        print('{:<7s}{:<30s}{}'.format(str(index), images, imagesize))
    return image_list

def list_entry():
    entry_id, entry_items, attached_image = [], [], []
    restore_types = ['restoredisk', 'restoreparts']
    with open("/pxe/tftp/boot.ipxe", "r") as pxe_file:
        for entry_line in pxe_file:
            if entry_line.startswith("item"):
                entry_id.append(entry_line.split(' ', 2)[1])
                entry_items.append(entry_line.split(' ', 2)[2])
            elif entry_line.startswith("choose"):
                current_default_entry = entry_line.split()[2]
                timeout = entry_line.split()[4]
                if timeout.isdigit():
                    timeout = int(int(timeout) / 1000)
                else:
                    timeout = "disabled"
    for id_find in entry_id:
        if id_find == 'shell' or id_find == 'exit':
            attached_image.append('')
        else:
            with open('/pxe/tftp/boot.ipxe', 'r') as f:
                for line in f:
                    if line.rstrip() == ":" + id_find:
                        restore_flag = False
                        kernel_entry = list(islice(f, 4))[-3].split()
                        for i, image_find in enumerate(kernel_entry):
                            if image_find in restore_types:
                                restore_flag = True
                                attached_image.append(kernel_entry[i+1])
                                break
                        if restore_flag == False:
                            attached_image.append('N/A')
    entry_items = [delimit.replace('\n', '') for delimit in entry_items]
    print("\nCurrent entries in PXE server:\n")
    fmt = '{:<13}{:<40}{}'
    print(fmt.format('Entry ID', 'Entry Name', 'Attached Restore Image'))
    for i, (list_id, list_entry, list_image) in enumerate(zip(entry_id, entry_items, attached_image)):
        print(fmt.format(list_id, list_entry, list_image))
    print("\nCurrent Default Entry: " + current_default_entry)
    print("Current Timeout set to (in seconds): " + str(timeout))
    return entry_id, entry_items, attached_image