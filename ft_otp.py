import argparse, sys

def parser():
    parser = argparse.ArgumentParser(
        prog='ft_otp',
        description='Generates TOTP codes based on a key'
    )
    parser.add_argument(
        '-g',
        dest='key_filename',
        help="Recursively downloads images from the URL.",
    )
    parser.add_argument(
        '-k',
        dest='encrypt',
        default=False, action='store_true',
        help="Create TOPT pass."
    )
    return parser.parse_args()

parsed_args = parser()
print(parsed_args)

KEY = parsed_args.key_filename
ENCRYPT = parsed_args.encrypt

if not KEY and not ENCRYPT:
    print("usage: ft_otp [-h] [-g KEY_FILENAME] [-k]", file=sys.stderr)
    sys.exit(1)


def handle_key():
    print("handle_key()")
        

if KEY:
    handle_key()

def open_key():
    print("open_key()")

def generate_otp():
    print("generate_otp()")

if ENCRYPT:
    open_key()
    generate_otp()

if __name__ == '__main__':
    print("FT_OTP")