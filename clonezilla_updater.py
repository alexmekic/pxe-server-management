import os, shutil, glob, re, requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

def check_clonezilla_update(current_version):
    if not current_version:
        print("Cannot check for Clonezilla updates. Clonezilla not installed")
    else:
        print("Checking for Clonezilla updates...")
        try:
            website_url = requests.get('https://clonezilla.org/downloads.php')
            soup = BeautifulSoup(website_url.content,'html5lib')
            latest_version = soup.find('a', attrs = {'href':'./downloads/download.php?branch=stable'}).find('font', attrs = {'color':'red'}).text
            if latest_version > current_version:
                print("New version of Clonezilla found: " + latest_version)
                update_option = input("Do you want to update Clonezilla? (y/n): ")
                if update_option == "y":
                    backup_clonezilla()
                    if update_clonezilla(latest_version):
                        print("Clonezilla updated to " + latest_version + " successfully")
                    elif not update_clonezilla(latest_version):
                        print("Clonezilla update failed")
                elif update_option == "n":
                    print("Clonezilla update aborted.")
            else:
                print("Latest version of Clonezilla already installed")
        except:
            print("Unable to check for updates")

def backup_clonezilla():
    current_clonezilla_dir = '/pxe/tftp/clonezilla'
    backup_clonezilla_dir = '/pxe/tftp/clonezilla_backup'
    if glob.glob(backup_clonezilla_dir):
        with open('/pxe/tftp/clonezilla_backup/Clonezilla-Live-Version') as f:
            backup_clonezilla_ver = f.readline()
        backup_clonezilla_ver = re.search('clonezilla-live-(.*)-amd64', backup_clonezilla_ver).group(1)
        while True:
            del_clonezilla_bak = input("Backup Clonezilla folder of version " + str(backup_clonezilla_ver) + " exists. Remove old version? (y/n): ")
            if del_clonezilla_bak == 'y':
                print('Removing old Clonezilla backup...', end='', flush=True)
                shutil.rmtree(backup_clonezilla_dir)
                print("Done")
                print("Backing up old version of Clonezilla...", end='', flush=True)
                shutil.copytree(current_clonezilla_dir, backup_clonezilla_dir)
                print("Done")
                break
            elif del_clonezilla_bak == 'n':
                return False
            else:
                print("Invalid selection")
    else:
        print("Backing up current version of Clonezilla...", end='', flush=True)
        shutil.copytree(current_clonezilla_dir, backup_clonezilla_dir)
        print("done")

def update_clonezilla(latest_version):
    print("Downloading new Clonezilla update...")
    url1 = 'http://free.nchc.org.tw/clonezilla-live/stable/clonezilla-live-' + str(latest_version) + '-amd64.zip'
    try:
        wget.download(url=url1, out='/pxe/tftp/clonezilla_update.zip')
        print('done')
    except:
        print("unable to download Clonezilla update.")
        return False
    print('Removing current version of Clonezilla...', end='', flush=True)
    shutil.rmtree('/pxe/tftp/clonezilla')
    print('Done')
    os.mkdir('/pxe/tftp/clonezilla')
    print('Extracting Clonezilla update...', end='', flush=True)
    with ZipFile('/pxe/tftp/clonezilla_update.zip', 'r') as zipObj:
        zipObj.extractall('/pxe/tftp/clonezilla')
    print('done')
    print('Cleaning up downloaded update file...', end='', flush=True)
    os.remove('/pxe/tftp/clonezilla_update.zip')
    print('done')
    return True

def revert_clonezilla():
    if glob.glob('/pxe/tftp/clonezilla_backup/Clonezilla-Live-Version'):
        with open('/pxe/tftp/clonezilla/Clonezilla-Live-Version') as f, open('/pxe/tftp/clonezilla_backup/Clonezilla-Live-Version') as f2:
            current_clonezilla_ver = f.readline()
            backup_clonezilla_ver = f2.readline()
        print("Current Clonezilla version installed: " + re.search('clonezilla-live-(.*)-amd64', current_clonezilla_ver).group(1))
        print("Previous Clonezilla version installed: " + re.search('clonezilla-live-(.*)-amd64', backup_clonezilla_ver).group(1))
        while True:
            revert_clonezilla_prompt = input("Are you sure you want to revert back to previous version of Clonezilla? (y/n): ")
            if revert_clonezilla_prompt == 'n':
                print("Operation aborted")
                break
            elif revert_clonezilla_prompt == 'y':
                print("Reverting Clonezilla to version " + re.search('clonezilla-live-(.*)-amd64', backup_clonezilla_ver).group(1) + "...", end='', flush=True)
                shutil.rmtree('/pxe/tftp/clonezilla')
                shutil.copytree('/pxe/tftp/clonezilla_backup/', '/pxe/tftp/clonezilla')
                print("done")
                break
            else:
                print("Invalid Option")
    else:
        print("No backup Clonezilla install found")