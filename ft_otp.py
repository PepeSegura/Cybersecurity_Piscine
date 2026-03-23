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
KEY_FILENAME = "ft_otp.key"
DECRYPT_KEY = ""


if not KEY and not ENCRYPT:
    print("usage: ft_otp [-h] [-g KEY_FILENAME] [-k]", file=sys.stderr)
    sys.exit(1)


def xor_encrypt_decrypt(hex_data, key):
    data = bytes.fromhex(hex_data)
    key_bytes = key.encode()
    result = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
    return result.hex()


def handle_key():
    try:
        infile = open(KEY, 'r')
        file_content = infile.read()
        infile.close()
        if len(file_content) != 64:
            raise Exception("key must be 64 hexadecimal characters.")
        for c in file_content.upper():
            if c not in "0123456789ABCDEF":
                raise Exception("key must be 64 hexadecimal characters.")
        outfile = open(KEY_FILENAME, 'w')
        outfile.write(xor_encrypt_decrypt(file_content, KEY_FILENAME))
        outfile.close()
    except Exception as e:
        print(f"./ft_otp: error: {e}")
        exit(1)
        

if KEY:
    handle_key()


def open_key():
    global DECRYPT_KEY
    try:
        key_file = open(KEY_FILENAME, 'r+')
        DECRYPT_KEY = key_file.read()
        key_file.close()
        print("DECRYPT_KEY: ", DECRYPT_KEY)
    except Exception as e:
        print(f"./ft_otp: error: {e}")


def generate_otp():
    print("generate_otp()")


if ENCRYPT:
    open_key()
    generate_otp()
