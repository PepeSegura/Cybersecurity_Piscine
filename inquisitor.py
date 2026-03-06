#! /usr/bin/python3

from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())


if __name__ == "__main__":
    print("inquisitor")
    sniff(prn=packet_callback, count=10)
