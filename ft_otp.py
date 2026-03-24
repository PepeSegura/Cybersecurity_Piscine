import argparse, sys
import time
import hmac
import hashlib

def parser():
    parser = argparse.ArgumentParser(
        prog='ft_otp',
        description='Generates TOTP codes based on a key'
    )
    parser.add_argument(
        '-g',
        dest='key_filename',
        help="Load key, encrypts it and stores it in ft_otp.key",
    )
    parser.add_argument(
        '-k',
        dest='encrypt',
        default=False, action='store_true',
        help="Create TOPT"
    )
    return parser.parse_args()


parsed_args = parser()

KEY_ARG = parsed_args.key_filename
ENCRYPT = parsed_args.encrypt


if not KEY_ARG and not ENCRYPT:
    print("usage: ft_otp [-h] [-g KEY_FILENAME] [-k]", file=sys.stderr)
    sys.exit(1)


def xor_encrypt_decrypt(hex_data, key):
    data = bytes.fromhex(hex_data)
    key_bytes = key.encode()
    result = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
    return result.hex()


KEY_FILENAME = "ft_otp.key"


def handle_key():
    try:
        infile = open(KEY_ARG, 'r')
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
    except FileNotFoundError as e:
        print(f"./ft_otp: error: No such file or directory: '{e.filename}'")
        exit(1)
    except Exception as e:
        print(f"./ft_otp: error: {e}")
        exit(1)


if KEY_ARG:
    handle_key()


def read_ft_otp_key():
    try:
        key_file = open(KEY_FILENAME, 'r+')
        key_content = key_file.read()
        key_file.close()
        return key_content
    except FileNotFoundError as e:
        print(f"./ft_otp: error: No such file or directory: '{e.filename}'")
        exit(1)
    except Exception as e:
        print(f"./ft_otp: error: {e}")
        exit(1)


def decrypt_key(encrypted_key) -> str:
    return xor_encrypt_decrypt(encrypted_key, KEY_FILENAME)


def get_K() -> str:
    encrypted_key = read_ft_otp_key()
    return decrypt_key(encrypted_key)


def get_T() -> int:
    current_unix_time = int(time.time())
    return (current_unix_time - 0) // 30


def HMAC_SHA_1(K:str, T:int):
    K_bytes = bytes.fromhex(K)
    T_bytes = T.to_bytes(8, byteorder='big')
    return hmac.new(K_bytes, T_bytes, hashlib.sha1).digest()


def truncate_hmac(hmac_result):
    offset = hmac_result[19] & 0xf
    bin_code = (
        (hmac_result[offset]   & 0x7f) << 24 |
        (hmac_result[offset+1] & 0xff) << 16 |
        (hmac_result[offset+2] & 0xff) <<  8 |
        (hmac_result[offset+3] & 0xff)
    )
    return bin_code % 10**6 


def generate_totp():
    totp = truncate_hmac(HMAC_SHA_1(get_K(), get_T()))
    print(totp)


if ENCRYPT:
    generate_totp()


"""
    TOTP = HOTP(K, T)
    T = (Current Unix time - T0) / X

    X represents the time step in seconds (default value X = 30 seconds) and is a system parameter.
    T0 is the Unix time to start counting time steps (default value is 0, i.e., the Unix epoch) and is also a system parameter.

    For example, with T0 = 0 and Time Step X = 30, T = 1 if the current
    Unix time is 59 seconds, and T = 2 if the current Unix time is 60 seconds.

    HOTP(K,C) = Truncate(HMAC-SHA-1(K,C))
    K and C represent the shared secret and counter value

    https://datatracker.ietf.org/doc/html/rfc6238#section-1.2
    https://datatracker.ietf.org/doc/html/rfc4226
"""
