from netifaces import interfaces, ifaddresses, AF_INET
from zfs_pool import PXE
import subprocess, os

def active_ip():
    ip_list, subnet_list = [], []
    for interface in interfaces():
        try:
            for link in ifaddresses(interface)[AF_INET]:
                ip_list.append(link['addr'])
                subnet_list.append(link['netmask'])
        except KeyError:
            continue
    for ip_check in ip_list:
        with open('/etc/rc.conf','r') as ip_conf_check:
            if ip_check in ip_conf_check.read():
                index = ip_list.index(ip_check)
                return ip_check, subnet_list[int(index)]

def get_image_partitions(image_dir):
    partition_list = []
    partitions = ' '
    with open(PXE.zfs_pool + '/images/' + image_dir + '/Info-saved-by-cmd.txt', 'r') as f:
        part_command = f.readline()
    for word in part_command.split():
        if word.startswith('sd'):
            partition_list.append(word)
        if 'saveparts' in word:
            restore_type = 'restoreparts'
        elif 'savedisk' in word:
            restore_type = 'restoredisk'
    return restore_type, (partitions.join(partition_list))
    
def zfs_health():
    zfs_state = os.popen("zpool status | grep state | awk '{print $2}'").read().strip()
    print("Current Disk Health state: " + zfs_state)
    zfs_online_errors = os.popen("zpool status | grep ONLINE | grep -v state | awk '{print $3 $4 $5}' | grep -v 000").read().strip()
    if zfs_state == "ONLINE" and zfs_online_errors:
        subprocess.call("zpool status", shell=True)
        print("Disk errors have been reported on the PXE storage pool. Review output above for further action required.")
        input("Press Enter to continue loading...")
        return True
    elif zfs_state == "DEGRADED" or zfs_state == "UNAVIL":
        subprocess.call("zpool status", shell=True)
        print("PXE storage pool is degraded. Please replace the bad disk from output above and wait for pool to be resilvered before running application again.")
        print("PXE Management Application halted")
        return False
    else:
        return True