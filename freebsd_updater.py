import subprocess, requests
from bs4 import BeautifulSoup

def check_package_patch_updates():
    print("Checking for package updates...")
    subprocess.call("sudo pkg upgrade", shell=True)
    print("\n")
    print("Checking for patch updates...")
    subprocess.call("sudo freebsd-update fetch", shell=True)
    command = subprocess.call("sudo freebsd-update install", shell=True)

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
        print('After first reboot, login as admin2/admin2 and type in the command "sudo freebsd-upgrade install" two more times to properly finish the upgrade process.')
    elif flag == 'major':
        print("WARNING! FreeBSD will be upgraded to major release " + latest_release)
        print("To proceed with upgrading, type Y four times total to continue when prompted if FreeBSD components installed and configuration are resonable, then hit Q multiple times when each list of components show up that will be upgraded/installed.")
        print('After first reboot, login as admin2/admin2 and type in the command "sudo freebsd-upgrade install" two more times to properly finish the upgrade process.')
    upgrade_option = input("Proceed to upgrade FreeBSD to " + latest_release + "? (y/n): ")
    if upgrade_option == 'y':
        subprocess.call("sudo freebsd-update upgrade -r " + latest_release + "-RELEASE", shell=True)
        subprocess.call("sudo freebsd-update install", shell=True)
        print("Rebooting server...")
        subprocess.call("sudo reboot", shell=True)
    elif upgrade_option == 'n':
        print("FreeBSD upgrade aborted.")