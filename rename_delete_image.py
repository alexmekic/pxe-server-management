import list_images_and_entries, glob, subprocess, os

def rename_image_name():
    image_list = list_images_and_entries.list_images()
    while True:
        old_image_rename = input("Enter image index (x to exit): ")
        if old_image_rename == "x":
            print("Operation aborted")
            break
        elif glob.glob("/pxe/images/" + image_list[int(old_image_rename)]):
            old_path = '/pxe/images/' + image_list[int(old_image_rename)]
            new_image_name = input("Enter new image name: ")
            new_path = '/pxe/images/' + new_image_name
            try:
                os.rename(old_path, new_path)
                print("Image renamed to " + new_image_name)
                return True
            except OSError:
                print("Error: New directory name already exists")
        else:
            print("Image not found")
            return False

def delete_image():
    while True:
        image_list = list_images_and_entries.list_images()
        image_index = input("Enter image name to delete (x to exit): ")
        if str(image_index) == "x":
            print("Operation aborted")
            break
        elif glob.glob('/pxe/images/' + (image_list[int(image_index)])):
            delete_confirm = input("WARNING! Are you sure you want to delete " + image_list[int(image_index)] + "? (y/n): ")
            if delete_confirm == 'y':
                print("Deleting " + image_list[int(image_index)] + "...", end='', flush=True)
                subprocess.call('sudo chmod -R 777 "/pxe/images/' + image_list[int(image_index)] + '"', shell=True)
                subprocess.call('sudo rm -R "/pxe/images/' + image_list[int(image_index)] + '"', shell=True)
                print("done")
                break
            elif delete_confirm == 'n':
                print("Operation aborted")
                break
        else:
            print("Invalid image index or image not found") 