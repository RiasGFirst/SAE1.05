from scapy.all import *
import subprocess
import ipaddress
import argparse


# Verify Sudo
def in_sudo_mode():
    """If the user doesn't run the program with super user privileges, don't allow them to continue."""
    if not 'SUDO_UID' in os.environ.keys():
        print("Try running this program with sudo.")
        exit()


# IP Forwarding
def allow_ip_forwarding():
    """ Run this function to allow ip forwarding. The packets will flow through your machine, and you'll be able to capture them. Otherwise user will lose connection."""
    # You would normally run the command sysctl -w net.ipv4.ip_forward=1 to enable ip forwarding. We run this with subprocess.run()
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"])
    # Load  in sysctl settings from the /etc/sysctl.conf file. 
    subprocess.run(["sysctl", "-p", "/etc/sysctl.conf"])


def active_discovery(target_ip):
    try:
        # Run the ping command and capture the standard output and standard error
        result = subprocess.run(["ping", "-c", "1", target_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the captured output and error
        print(result.stdout)
        print(result.stderr)

        if result.returncode == 0:
            print(f"Host {target_ip} is reachable.")
        else:
            print(f"Host {target_ip} is not reachable.")
        
        # Return the captured output and error
        return result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return e


# Passive Discovery 
def passive_discovery(target_ip):
    res = ""
    try:
        print(f"Starting passive discovery for {target_ip} using ARP...")
        arp_request = ARP(pdst=target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp_request
        result = srp(packet, timeout=3, verbose=0)[0]

        for sent, received in result:
            print(f"Host {received.psrc} is online.")
            res = f"Starting passive discovery for {target_ip} using ARP...\nHost {received.psrc} is online."

        return res
    except Exception as e:
        print(f"Error: {e}")
        return e


# Check connected device on Network
def network_discovery(ip_range):
    arp_responses = list()
    answered_lst = arping(ip_range, verbose=0)[0]
    print(answered_lst)
    for res in answered_lst:
        arp_responses.append({"ip" : res[1].psrc, "mac" : res[1].hwsrc})

    for id, res in enumerate(arp_responses):
        print("ID: {} IP: {} MAC: {}".format(id, res['ip'], res['mac']))
        #print(type(res))
    # We return the list of arp responses which contains dictionaries for every arp response.
    return arp_responses


# Work On It...........
def export_results(results, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(results)
        print(f"Results exported to {output_file}.")
    except Exception as e:
        print(f"Error: {e}")


def run_main():

    in_sudo_mode()
    allow_ip_forwarding()

    parser = argparse.ArgumentParser(description="Host Discovery Script")
    parser.add_argument("-a", "--active", metavar="TARGET_IP", help="Activate active discovery for the specified target IP.")
    parser.add_argument("-p", "--passive", metavar="TARGET_IP", help="Activate passive discovery for the specified target IP.")
    parser.add_argument("-t", "--test", metavar="NETWORK", help="Test the presence of hosts in the specified network using ICMP.")
    parser.add_argument("-x", "--export", metavar="OUTPUT_FILE", help="Export results to the specified file.")

    args = parser.parse_args()

    if args.export:
        if args.active or args.passive or args.test:
            # If any of the active, passive, or test options are used along with -x, export the respective results.
            result = None
            if args.active:
                result = active_discovery(args.active)
            elif args.passive:
                result = passive_discovery(args.passive)
            elif args.test:
                res = network_discovery(args.test)
                result=""
                for dev in res:
                    result +=f"IP: {dev['ip']} / MAC: {dev['mac']}\n"

            # Check if the result is not None before exporting.
            if result:
                export_results(result, args.export)
        else:
            print("You need to specify either -a, -p, or -t along with -x to export results.")
    else:
        if args.active:
            active_discovery(args.active)
        if args.passive:
            passive_discovery(args.passive)
        if args.test:
            network_discovery(args.test)

if __name__ == "__main__":
    run_main()
