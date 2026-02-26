import argparse, sys

def parser():
    parser = argparse.ArgumentParser(
        prog='scorpion',
        description='Shows the metadata from the given img files'
    )
    parser.add_argument(
        '-r',
        dest='recursive_enable',
        default=False, action='store_true',
        help="Recursively downloads images from the URL.",
    )
    parser.add_argument(
        'FILES', metavar='FILE',
        nargs='+', type=str,
        help='Input files to show metadaba about'
    )
    return parser.parse_args()


parsed_args = parser()

FILES = parsed_args.FILES

def identify_type(binary_file) -> str:
    magic_numbers = {
        b'\xFF\xD8\xFF\xE0': '.jpg/JFIF(APP0)',
        b'\xFF\xD8\xFF\xE1': '.jpg/Exif(APP1)',
        b'\xFF\xD8\xFF\xE2': '.jpg/Canon/ICC(APP2)',
        b'\xFF\xD8\xFF\xDB': '.jpg/DQT',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': '.png',
        b'\x47\x49\x46\x38\x37\x61': '.gif1',
        b'\x47\x49\x46\x38\x39\x61': '.gif2',
        b'\x42\x4D': '.bmp'
    }

    for signature, extension in magic_numbers.items():
        if binary_file.startswith(signature):
            print("FILE: ", extension)
            return extension
    return 'none'


def parse_jpg_JFIF_APP0():
    print("Parsing jpg/JFIF(APP0)")


def parse_jpg_Exif_APP1():
    print("Parsing jpg/Exif(APP1)")


def parse_jpg_Canon_ICC_APP2():
    print("Parsing jpg/Canon/ICC(APP2)")


def parse_jpg_DQT():
    print("Parsing jpg/DQT")


def parse_png():
    print("Parsing png")


def parse_gif1():
    print("Parsing gif1")


def parse_gif2():
    print("Parsing gif2")


def parse_bmp():
    print("Parsing bmp")

def parse_error():
    print("File format not supported")
    sys.exit(1)


def choose_file_parser(extension):
    functions = {
        '.jpg/JFIF(APP0)': parse_jpg_JFIF_APP0,
        '.jpg/Exif(APP1)': parse_jpg_Exif_APP1,
        '.jpg/Canon/ICC(APP2)': parse_jpg_Canon_ICC_APP2,
        '.jpg/DQT': parse_jpg_DQT,
        '.png':  parse_png,
        '.gif1': parse_gif1,
        '.gif2': parse_gif2,
        '.bmp':  parse_bmp,
        'none':  parse_error
    }
    if extension not in functions:
        print(f"Invalid extension: {extension}")
        return
    functions[extension]()

def get_metadata(filename):
    with open(filename, 'rb') as file:
        bynary_data = file.read(100)
        choose_file_parser(identify_type(bynary_data))
        print(bynary_data)

if __name__ == '__main__':
    for file in FILES:
        print(f"Getting metadata for {file}")
        get_metadata(file)