import argparse

def parse_args():
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
