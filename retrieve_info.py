from netifaces import interfaces, ifaddresses, AF_INET

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
    with open('/pxe/images/' + image_dir + '/Info-saved-by-cmd.txt', 'r') as f:
        part_command = f.readline()
    for word in part_command.split():
        if word.startswith('sd'):
            partition_list.append(word)
        if 'saveparts' in word:
            restore_type = 'restoreparts'
        elif 'savedisk' in word:
            restore_type = 'restoredisk'
    return restore_type, (partitions.join(partition_list))