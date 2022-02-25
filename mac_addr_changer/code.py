import random
import subprocess
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac addr")
    (options, arguments) = parser.parse_args()
    interface = options.interface
    new_mac = options.new_mac

    if interface and new_mac:
        return (interface,new_mac)
    else:
        interface = input("interface > ")
        choice = input("Do you want a random MAC or yours? r/y: ")
        if choice == "y":
            new_mac = input("New MAC: ")
            return (interface, new_mac)
        else:
            a,b,c,d,e = random.randint(10,99), random.randint(10,99), random.randint(10,99), random.randint(10,99), random.randint(10,99)
            new_mac = f'00:{a}:{b}:{c}:{d}:{e}'
            return (interface, new_mac)


def mac_changer(interface ,new_mac):
    print(f"[+] Changing MAC addres for {interface} to " + new_mac)
    subprocess.call(["sudo", 'ifconfig', interface, "down"])
    subprocess.call(["sudo", 'ifconfig', interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, 'up'])

arg = get_arguments()
mac_changer(arg[0], arg[1])
