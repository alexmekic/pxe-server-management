import subprocess, shutil

def is_valid_ipv4_address(ip_address):
    octets = ip_address.split(".")
    return len(octets) == 4 and all(o.isdigit() and 0 <= int(o) < 256 for o in octets)

def is_valid_netmask_address(netmask):
    if not is_valid_ipv4_address(netmask):
        return False
    a, b, c, d = (int(octet) for octet in netmask.split("."))
    mask = a << 24 | b << 16 | c << 8 | d
    if mask == 0:
        return False
    m = mask & -mask
    right0bits = -1
    while m:
        m >>= 1
        right0bits += 1
    if mask | ((1 << right0bits) - 1) != 0xffffffff:
        return False
    return True

def change_ip_address(old_ip_address, old_netmask):
    while True:
        new_ip_address = input("Enter new static IP address (x to exit): ")
        if new_ip_address == 'x':
            print("Operation aborted")
            break
        elif is_valid_ipv4_address(new_ip_address):
            while True:
                new_netmask = input("Enter new netmask: ")
                if is_valid_netmask_address(new_netmask):
                    subprocess.call("sudo sed -i '' 's/" + old_ip_address + "/" + new_ip_address + "/g' /etc/rc.conf", shell=True)
                    subprocess.call("sudo sed -i '' 's/" + old_netmask + "/" + new_netmask + "/g' /etc/rc.conf", shell=True)
                    subprocess.call("sudo sed -i '' 's/" + old_ip_address + "/" + new_ip_address + "/g' /usr/local/etc/dnsmasq.conf", shell=True)
                    shutil.copy2('/pxe/tftp/boot.ipxe', '/pxe/tftp/boot.ipxe.bak')
                    subprocess.call("sudo sed -i '' 's/" + old_ip_address + "/" + new_ip_address + "/g' /pxe/tftp/boot.ipxe", shell=True)
                    print("Static IP address changed to " + new_ip_address + " with netmask " + new_netmask)
                    break
                else:
                    print("Invalid Netmask Address")
            while True:
                reboot_prompt = input("PXE server reboot is recommended. Reboot? (y/n): ")
                if reboot_prompt == 'y':
                    print("Rebooting server...")
                    subprocess.call('sudo reboot', shell=True)
                elif reboot_prompt == 'n':
                    print("Restarting networking service...")
                    subprocess.call('sudo service netif restart', shell=True)
                    print("done")
                    break
                else:
                    print("Invalid Option")
        else:
            print("Invalid IP Address")

def change_dhcp_range():
    with open('/usr/local/etc/dnsmasq.conf') as f:
        for line in f:
            if 'dhcp-range' in line:
                old_start_ip = line.split("=")[1].split(",")[0]
                old_end_ip = line.split("=")[1].split(",")[1]
    print("Current DHCP IP address range configured: " + old_start_ip + " - " + old_end_ip)
    while True:
        new_start_ip = input('Enter new starting IP DHCP range (x to exit): ')
        if new_start_ip == 'x':
            print("Operation aborted")
            break
        elif is_valid_ipv4_address(new_start_ip):
            new_end_ip = input('Enter new ending IP DHCP range: ')
            if is_valid_ipv4_address(new_end_ip) and new_end_ip > new_start_ip:
                subprocess.call("sudo sed -i '' 's/" + old_start_ip + "/" + new_start_ip + "/g' /usr/local/etc/dnsmasq.conf", shell=True)
                subprocess.call("sudo sed -i '' 's/" + old_end_ip + "/" + new_end_ip + "/g' /usr/local/etc/dnsmasq.conf", shell=True)
                print("DHCP range update to " + new_start_ip + " - " + new_end_ip)
                print("Restarting DHCP server...")
                subprocess.call("sudo service dnsmasq restart", shell=True)
                break
            elif not is_valid_ipv4_address(new_end_ip):
                print("Invalid IP Address")
            else:
                print("End IP DHCP range address not greater than beginning IP DHCP range address")
        else:
            print("Invalid IP Address")