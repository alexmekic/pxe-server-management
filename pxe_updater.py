import os, shutil, glob, re, requests, wget, subprocess, json
from zipfile import ZipFile
from bs4 import BeautifulSoup
from zfs_pool import PXE

def check_management_update(current_version):
    print("Checking for PXE Management Application updates...", end='', flush=True)
    try:
        website_url = "https://api.github.com/repos/alexmekic/clonezillaserver-management/releases"
        latest_version = json.loads(requests.get(website_url).text)[0]['tag_name']
        url_download = "https://github.com/alexmekic/clonezillaserver-management/releases/download/" + latest_version + "/pxe_management"
        print('done')
        if latest_version > current_version:
            print("New version of PXE Management found: " + latest_version)
            update_option = input("Update PXE Management Application? (y/n): ")
            if update_option == "y":
                try:
                    print("Backing up current version...", end='', flush=True)
                    shutil.copy2(PXE.zfs_pool + '/pxe_management/pxe_management', PXE.zfs_pool + '/pxe_management/pxe_management.bak')
                    print("done")
                    print("Downloading new version of PXE Management...")
                    wget.download(url=url_download, out=PXE.zfs_pool + '/pxe_management/pxe_management_update')
                    print("done")
                    print("Upgrading new version of PXE Management...", end='', flush=True)
                    os.remove(PXE.zfs_pool + '/pxe_management/pxe_management')
                    os.rename(PXE.zfs_pool + '/pxe_management/pxe_management_update', PXE.zfs_pool + '/pxe_management/pxe_management')
                    subprocess.call('chmod +x ' + PXE.zfs_pool + '/pxe_management/pxe_management', shell=True)
                    print("done")
                    print("PXE Management Application update to " + latest_version + " successful")
                    print("Log out or restart server to load update application")
                except:
                    print("failed")
            elif update_option == "n":
                print("PXE Management Application update aborted.")
        else:
            print("Latest version of PXE Management already installed")
    except:
        print("failed")

def check_clonezilla_update(current_version):
    if not current_version:
        print("Cannot check for Clonezilla updates. Clonezilla not installed")
    else:
        print("Checking for Clonezilla updates...", end='', flush=True)
        try:
            website_url = requests.get('https://clonezilla.org/downloads.php')
            soup = BeautifulSoup(website_url.content,'html5lib')
            latest_version = soup.find('a', attrs = {'href':'./downloads/download.php?branch=stable'}).find('font', attrs = {'color':'red'}).text
            print("done")
            if latest_version > current_version:
                print("New version of Clonezilla found: " + latest_version)
                update_option = input("Do you want to update Clonezilla? (y/n): ")
                if update_option == "y":
                    if backup_clonezilla():
                        update_clonezilla(latest_version)
                elif update_option == "n":
                    print("Clonezilla update aborted.")
            else:
                print("Latest version of Clonezilla already installed")
        except:
            print("Unable to check for updates")

def backup_clonezilla():
    current_clonezilla_dir = PXE.zfs_pool + '/tftp/clonezilla'
    backup_clonezilla_dir = PXE.zfs_pool + '/tftp/clonezilla_backup'
    if glob.glob(backup_clonezilla_dir):
        with open(PXE.zfs_pool + '/tftp/clonezilla_backup/Clonezilla-Live-Version') as f:
            backup_clonezilla_ver = f.readline()
        backup_clonezilla_ver = re.search('clonezilla-live-(.*)-amd64', backup_clonezilla_ver).group(1)
        while True:
            del_clonezilla_bak = input("Backup Clonezilla folder of version " + str(backup_clonezilla_ver) + " exists. Remove old version? (y/n): ")
            if del_clonezilla_bak == 'y':
                print('Removing old Clonezilla backup...', end='', flush=True)
                shutil.rmtree(backup_clonezilla_dir)
                print("done")
                print("Backing up old version of Clonezilla...", end='', flush=True)
                shutil.copytree(current_clonezilla_dir, backup_clonezilla_dir)
                print("done")
                return True
            elif del_clonezilla_bak == 'n':
                return False
            else:
                print("Invalid selection")
    else:
        try:
            print("Backing up current version of Clonezilla...", end='', flush=True)
            shutil.copytree(current_clonezilla_dir, backup_clonezilla_dir)
            print("done")
            return True
        except:
            print("failed")
            return False

def update_clonezilla(latest_version):
    print("Downloading new Clonezilla update...")
    url_download = 'https://sourceforge.net/projects/clonezilla/files/clonezilla_live_stable/' + str(latest_version) + '/clonezilla-live-' + str(latest_version) + '-amd64.zip/download'
    try:
        wget.download(url=url_download, out=PXE.zfs_pool + '/tftp/clonezilla_update.zip')
        print('done')
        print('Upgrading version of Clonezilla...', end='', flush=True)
        shutil.rmtree(PXE.zfs_pool + '/tftp/clonezilla')  
        os.mkdir(PXE.zfs_pool + '/tftp/clonezilla')
        with ZipFile(PXE.zfs_pool + '/tftp/clonezilla_update.zip', 'r') as zipObj:
            zipObj.extractall(PXE.zfs_pool + '/tftp/clonezilla')
        print('done')
        print('Cleaning up downloaded update file...', end='', flush=True)
        os.remove(PXE.zfs_pool + '/tftp/clonezilla_update.zip')
        print('done')
        print("Clonezilla updated to " + latest_version + " successful")
        return True
    except:
        print("failed")
        return False

def revert_clonezilla():
    if glob.glob(PXE.zfs_pool + '/tftp/clonezilla_backup/Clonezilla-Live-Version'):
        with open(PXE.zfs_pool + '/tftp/clonezilla/Clonezilla-Live-Version') as f, open(PXE.zfs_pool + '/tftp/clonezilla_backup/Clonezilla-Live-Version') as f2:
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
                shutil.rmtree(PXE.zfs_pool + '/tftp/clonezilla')
                shutil.copytree(PXE.zfs_pool + '/tftp/clonezilla_backup/', PXE.zfs_pool + '/tftp/clonezilla')
                print("done")
                break
            else:
                print("Invalid Option")
    else:
        print("No backup Clonezilla install found")

def check_package_patch_updates():
    print("Checking for package updates...")
    subprocess.call("sudo pkg upgrade", shell=True)
    print("\n")
    print("Checking for patch updates...")
    subprocess.call("sudo freebsd-update fetch", shell=True)
    subprocess.call("sudo freebsd-update install", shell=True)

def check_freebsd_updates(current_version):
    print("Checking for FreeBSD Updates...")
    try:
        website_url = requests.get('https://download.freebsd.org/ftp/releases/amd64/amd64/ISO-IMAGES/').text
        soup = BeautifulSoup(website_url,'lxml')
        table = soup.find('table',{'id':'list'})
        release_table = table.findAll('a')
        freebsd_releases = []
        for releases in release_table:
            if releases.get('title') != None:
                freebsd_releases.append(releases.get('title'))
            else:
                continue
        latest_release = freebsd_releases[-1]
        if latest_release == current_version:
            print("No FreeBSD upgrades found. Latest version already installed.")
        elif int(float(latest_release)) - int(float(current_version)) == 0:
            print("FreeBSD " + latest_release + "minor upgrade found.\n")
            flag = 'minor'
            upgrade_freebsd(latest_release, flag)
        elif int(float(latest_release)) - int(float(current_version)) != 0:
            print("FreeBSD " + latest_release + "major upgrade found.\n")
            flag = 'major'
            upgrade_freebsd(latest_release, flag)
    except:
        print("Unable to check updates")
    
def upgrade_freebsd(latest_release, flag):
    if flag == 'minor':
        print("Warning! FreeBSD will be upgraded to minor release " + latest_release)
        print("To proceed with upgrading, type Y to continue when prompted if FreeBSD components installed are resonable, then hit Q multiple times when each list of components show up that will be upgraded/installed.")
        print('After first reboot, login as either root or the admin account, exit to shell and type in the command "sudo freebsd-upgrade install" two more times to properly finish the upgrade process.')
    elif flag == 'major':
        print("WARNING! FreeBSD will be upgraded to major release " + latest_release)
        print("To proceed with upgrading, type Y four times total to continue when prompted if FreeBSD components installed and configuration are resonable, then hit Q multiple times when each list of components show up that will be upgraded/installed.")
        print('After first reboot, login as either root or the admin account, exit to shell and type in the command "sudo freebsd-upgrade install" two more times to properly finish the upgrade process.')
    upgrade_option = input("Proceed to upgrade FreeBSD to " + latest_release + "? (y/n): ")
    if upgrade_option == 'y':
        subprocess.call("sudo freebsd-update upgrade -r " + latest_release + "-RELEASE", shell=True)
        subprocess.call("sudo freebsd-update install", shell=True)
        print("Rebooting server...")
        subprocess.call("sudo reboot", shell=True)
    elif upgrade_option == 'n':
        print("FreeBSD upgrade aborted.")