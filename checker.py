import pyotp
import base64
import binascii

def xor_encrypt_decrypt(hex_data, key):
    data = bytes.fromhex(hex_data)
    key_bytes = key.encode()
    result = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
    return result.hex()

KEY_FILENAME = "ft_otp.key"

try:
    with open(KEY_FILENAME, 'r') as key_file:
        encrypted_hex_key = key_file.read().strip()
except Exception as e:
    print(f"Error: {e}")
    exit(1)

decrypted_hex_key = xor_encrypt_decrypt(encrypted_hex_key, KEY_FILENAME)
raw_bytes = binascii.unhexlify(decrypted_hex_key)
base32_secret = base64.b32encode(raw_bytes).decode('utf-8')
totp = pyotp.TOTP(base32_secret)
print(f"{totp.now()}")
