import list_images_and_entries
import glob, subprocess, os
from zfs_pool import PXE

def rename_image_name():
    image_list = list_images_and_entries.list_images()
    while True:
        try:
            old_image_rename = input("Enter image index (x to exit): ")
            if old_image_rename == "x":
                print("Operation aborted")
                break
            else:
                old_path = PXE.zfs_pool + '/images/' + image_list[int(old_image_rename)]
                new_image_name = input("Enter new image name: ")
                new_path = PXE.zfs_pool + '/images/' + new_image_name
                try:
                    os.rename(old_path, new_path)
                    print("Image renamed to " + new_image_name)
                    break
                except OSError:
                    print("Error: New directory name already exists")
        except:
            print("Image not found")

def delete_image():
    while True:
        try:
            image_list = list_images_and_entries.list_images()
            image_index = input("Enter image name to delete (x to exit): ")
            if str(image_index) == "x":
                print("Operation aborted")
                break
            else:
                delete_confirm = input("WARNING! Are you sure you want to delete " + image_list[int(image_index)] + "? (y/n): ")
                if delete_confirm == 'y':
                    print("Deleting " + image_list[int(image_index)] + "...", end='', flush=True)
                    subprocess.call('sudo rm -R /' + PXE_.PXE_DIRECTORY + '/images/' + image_list[int(image_index)] + '"', shell=True)
                    print("done")
                    break
                elif delete_confirm == 'n':
                    print("Operation aborted")
                    break
        except:
            print("Invalid image index or image not found")
