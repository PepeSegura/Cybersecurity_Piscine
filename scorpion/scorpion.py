import argparse, sys, struct, os, time


def parser():
    parser = argparse.ArgumentParser(
        prog='scorpion',
        description='Shows the metadata from the given img files'
    )
    parser.add_argument(
        'FILES', metavar='FILE',
        nargs='+', type=str,
        help='Input files to show metadaba about'
    )
    return parser.parse_args()


parsed_args = parser()

FILES = parsed_args.FILES

def identify_type(binary_file:memoryview) -> str:
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
        if bytes(binary_file).startswith(signature):
            return extension
    return None


def return_hex(BYTES:memoryview):
    # return hex(int.from_bytes(BYTES)).upper()
    return " ".join(f"{x:02X}" for x in bytes(BYTES))


def decode_unsigned_byte(raw_data:memoryview, count:int, endian:str, tag_name:str):
    values = list(raw_data)
    return values if count > 1 else values[0]


def decode_ascii_string(raw_data:memoryview, count:int, endian:str, tag_name:str):
    return bytes(raw_data).rstrip(b"\x00").decode(errors="ignore")


def decode_unsigned_short(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}H"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_unsigned_long(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}I"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_unsigned_rational(raw_data:memoryview, count:int, endian:str, tag_name:str):
    values = []
    for i in range(count):
        num = int.from_bytes(raw_data[i*8:i*8+4], endian)
        den = int.from_bytes(raw_data[i*8+4:i*8+8], endian)
        values.append(num / den if den else 0)
    return values if count > 1 else values[0]


def decode_signed_byte(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}b"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_undefined(raw_data:memoryview, count:int, endian:str, tag_name:str):
    if tag_name == "ExifVersion":
        return bytes(raw_data).decode("ascii", errors="ignore").strip()
    if tag_name == "ComponentConfiguration":
        return return_hex(raw_data)
    if tag_name == "FlashPixVersion":
        return bytes(raw_data).decode("ascii", errors="ignore").strip()
    if tag_name == "UserComment":
        return bytes(raw_data).decode("ascii", errors="ignore").strip()
    return return_hex(raw_data)


def decode_signed_short(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}h"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_signed_long(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}i"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_signed_rational(raw_data:memoryview, count:int, endian:str, tag_name:str):
    values = []
    for i in range(count):
        num = int.from_bytes(raw_data[i*8:i*8+4], endian, signed=True)
        den = int.from_bytes(raw_data[i*8+4:i*8+8], endian, signed=True)
        values.append(num / den if den else 0)
    return values if count > 1 else values[0]


def decode_single_float(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}f"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_double_float(raw_data:memoryview, count:int, endian:str, tag_name:str):
    fmt = ("<" if endian == "little" else ">") + f"{count}d"
    values = struct.unpack(fmt, raw_data)
    return values if count > 1 else values[0]


def decode_unknown(raw_data:memoryview, count:int, endian:str, tag_name:str):
    return bytes(raw_data)

IFD_DATA_FORMATS = {
    1:  (1, "unsigned byte", decode_unsigned_byte),
    2:  (1, "ascii string", decode_ascii_string),
    3:  (2, "unsigned short", decode_unsigned_short),
    4:  (4, "unsigned long", decode_unsigned_long),
    5:  (8, "unsigned rational", decode_unsigned_rational),
    6:  (1, "signed byte", decode_signed_byte),
    7:  (1, "undefined", decode_undefined),
    8:  (2, "signed short", decode_signed_short),
    9:  (4, "signed long", decode_signed_long),
    10: (8, "signed rational", decode_signed_rational),
    11: (4, "single float", decode_single_float),
    12: (8, "double float", decode_double_float)
}

IFD_DEFAULT_FORMAT = (1, "None", decode_unknown)

TAGS_IFD = {

    # Tags used by IFD0 (main image)
    0x010E: "ImageDescription",
    0x010F: "Make",
    0x0110: "Model",
    0x0112: "Orientation",      # The start point of stored data is, '1' means upper left, '3' lower right, '6' upper right, '8' lower left, '9' undefined.
    0x011a: "XResolution",
    0x011b: "YResolution",
    0x0128: "ResolutionUnit",
    0x0131: "Software",
    0x0132: "DateTime",         # Date/Time of image was last modified. Data format is "YYYY:MM:DD HH:MM:SS"+0x00, total 20bytes.
    0x013e: "WhitePoint",
    0x013f: "PrimaryChromaticities",
    0x0211: "YCbCrCoefficients",
    0x0213: "YCbCrPositioning",
    0x0214: "ReferenceBlackWhite",
    0x8298: "Copyright",
    0x8769: "ExifOffset",

    # Tags used by Exif SubIFD
    0x829a: "ExposureTime",
    0x829d: "FNumber",
    0x8822: "ExposureProgram",
    0x8827: "ISOSpeedRatings",
    0x9000: "ExifVersion",
    0x9003: "DateTimeOriginal",
    0x9004: "DateTimeDigitized",
    0x9101: "ComponentConfiguration",
    0x9102: "CompressedBitsPerPixel",
    0x9201: "ShutterSpeedValue",
    0x9202: "ApertureValue",
    0x9203: "BrightnessValue",
    0x9204: "ExposureBiasValue",
    0x9205: "MaxApertureValue",
    0x9206: "SubjectDistance",
    0x9207: "MeteringMode",
    0x9208: "LightSource",
    0x9209: "Flash",
    0x920a: "FocalLength",
    0x927c: "MakerNote",
    0x9286: "UserComment",
    0xa000: "FlashPixVersion",
    0xa001: "ColorSpace",
    0xa002: "ExifImageWidth",
    0xa003: "ExifImageHeight",
    0xa004: "RelatedSoundFile",
    0xa005: "ExifInteroperabilityOffset",
    0xa20e: "FocalPlaneXResolution",
    0xa20f: "FocalPlaneYResolution",
    0xa210: "FocalPlaneResolutionUnit",
    0xa217: "SensingMethod",
    0xa300: "FileSource",       # Unknown but value is '3'.
    0xa301: "SceneType",        # Unknown but value is '1'.

    # Tags used by IFD1 (thumbnail image)
    0x0100:	"ImageWidth",
    0x0101:	"ImageLength",
    0x0102:	"BitsPerSample",
    0x0103:	"Compression",
    0x0106:	"PhotometricInterpretation",
    0x0111:	"StripOffsets",
    0x0115:	"SamplesPerPixel",
    0x0116:	"RowsPerStrip",
    0x0117:	"StripByteConunts",
    0x011a:	"XResolution",
    0x011b:	"YResolution",
    0x011c:	"PlanarConfiguration",
    0x0128:	"ResolutionUnit",
    0x0201:	"JpegIFOffset",
    0x0202:	"JpegIFByteCount",
    0x0211:	"YCbCrCoefficients",
    0x0212:	"YCbCrSubSampling",
    0x0213:	"YCbCrPositioning",
    0x0214:	"ReferenceBlackWhite",

    # Misc Tags
    0x00fe:	"NewSubfileType",
    0x00ff:	"SubfileType",
    0x012d:	"TransferFunction",
    0x013b:	"Artist",
    0x013d:	"Predictor",
    0x0142:	"TileWidth",
    0x0143:	"TileLength",
    0x0144:	"TileOffsets",
    0x0145:	"TileByteCounts",
    0x014a:	"SubIFDs",
    0x015b:	"JPEGTables",
    0x828d:	"CFARepeatPatternDim",
    0x828e:	"CFAPattern",
    0x828f:	"BatteryLevel",
    0x83bb:	"IPTC/NAA",
    0x8773:	"InterColorProfile",
    0x8824:	"SpectralSensitivity",
    0x8825:	"GPSInfo",
    0x8828:	"OECF",
    0x8829:	"Interlace",
    0x882a:	"TimeZoneOffset",
    0x882b:	"SelfTimerMode",
    0x920b:	"FlashEnergy",
    0x920c:	"SpatialFrequencyResponse",
    0x920d:	"Noise",
    0x9211:	"ImageNumber",
    0x9212:	"SecurityClassification",
    0x9213:	"ImageHistory",
    0x9214:	"SubjectLocation",
    0x9215:	"ExposureIndex",
    0x9216:	"TIFF/EPStandardID",
    0x9290:	"SubSecTime",
    0x9291:	"SubSecTimeOriginal",
    0x9292:	"SubSecTimeDigitized",
    0xa20b:	"FlashEnergy",
    0xa20c:	"SpatialFrequencyResponse",
    0xa214:	"SubjectLocation",
    0xa215:	"ExposureIndex",
    0xa302:	"CFAPattern ",
}



def read_ifd_value(DATA:memoryview, tiff_start_pos: int, entry_offset:int, data_type:int, count:int, endian, tag_name:str):
    value_field_offset = entry_offset + 8
    data_format_size, data_format_name, decoder = IFD_DATA_FORMATS.get(data_type, IFD_DEFAULT_FORMAT)
    total_size = data_format_size * count

    if total_size <= 4:
        raw_data = DATA[value_field_offset:value_field_offset + total_size]
    else:
        data_offset = int.from_bytes(
            DATA[value_field_offset:value_field_offset + 4],
            endian
        )
        raw_data = DATA[tiff_start_pos + data_offset: tiff_start_pos + data_offset + total_size]

    return decoder(raw_data, count, endian, tag_name)


def parse_ifd(DATA: memoryview, tiff_start:int, ifd_offset:int, endian:str, name:str="IFD"):
    print(f"\n----- [{name}] -----")

    base_offset = tiff_start + ifd_offset
    entries_count = int.from_bytes(DATA[base_offset:base_offset+2], endian)

    print(f"Number of entries: {entries_count}")
    for i in range(entries_count):
        entry_offset = base_offset + 2 + (i * 12)

        tag = int.from_bytes(DATA[entry_offset:entry_offset + 2], endian)
        tag_name = TAGS_IFD.get(tag, "UnkownTag")
        data_type = int.from_bytes(DATA[entry_offset + 2:entry_offset + 4], endian)
        data_count = int.from_bytes(DATA[entry_offset + 4:entry_offset + 8], endian)


        value = read_ifd_value(
            DATA,
            tiff_start,
            entry_offset,
            data_type,
            data_count,
            endian,
            tag_name
        )

        print(f"{tag_name.ljust(26)}: {value}")

        if tag_name == "ExifOffset":
            parse_ifd(DATA, tiff_start, value, endian, "Exif SubIFD")
        if tag_name == "GPSInfo":
            parse_ifd(DATA, tiff_start, value, endian, "GPS SubIFD")
        if tag_name == "SubIFDs":
            parse_ifd(DATA, tiff_start, value, endian, "SubIFDs")
    
    next_ifd_offset = int.from_bytes(
        DATA[
            base_offset + 2 + (entries_count * 12):
            base_offset + 2 + (entries_count * 12) + 4
        ],
        endian
    )

    if next_ifd_offset != 0:
        parse_ifd(
            DATA,
            tiff_start,
            next_ifd_offset,
            endian,
            "Next IFD",
        )


def APP1_DATA(DATA:memoryview):
    """
        Parser for the APP1 Segment (Marker + Size + Data)
    """

    exif_header = DATA[0:6]
    print(f"Exif header: {return_hex(exif_header)} ({bytes(exif_header)})")

    # TIFF: Tagged Image File Format
    tiff_start_pos = 6
    tiff_size = 8
    tiff_header = DATA[tiff_start_pos:(tiff_start_pos + tiff_size)]
    tiff_alignment = tiff_header[0:2]
    tiff_alignment_str = "big" if bytes(tiff_alignment) == b"MM" else "little"
    tiff_tag = tiff_header[2:(2+2)]
    tiff_offset_first_IFD = tiff_header[4:(4+4)]
    print(f"Tiff header: {return_hex(tiff_header)} ({bytes(tiff_header)})")
    print(f"Tiff header: {return_hex(tiff_alignment)} ({bytes(tiff_alignment)}) '{tiff_alignment_str}'")
    print(f"Tiff header: {return_hex(tiff_tag)} ({bytes(tiff_tag)})")
    print(f"Tiff header: {return_hex(tiff_offset_first_IFD)} ({bytes(tiff_offset_first_IFD)})")

    parse_ifd(
        DATA,
        tiff_start_pos,
        int.from_bytes(tiff_offset_first_IFD, tiff_alignment_str),
        tiff_alignment_str,
        "IDF0"
    )


def parse_jpg_Exif_APP1(binary_file:memoryview, filename):
    print("Parsing jpg/Exif(APP1)")
    soi = bytes(binary_file[:2])                            # 0xFFD8
    marker = bytes(binary_file[2:4])                        # 0xFFD1
    size_bytes = bytes(binary_file[4:6])                    # 0xSSSS
    size_int = int.from_bytes(size_bytes, byteorder="big")  # 260

    # APP1 segment Data
    app1_segment = binary_file[6:(4 + size_int)]
    APP1_DATA(app1_segment)


def print_basic_info(filename):
    stats = os.stat(filename)
    print(f"Size: {stats.st_size} bytes, Modified: {time.ctime(stats.st_mtime)}")


def parse_jpg_JFIF_APP0(binary_file:memoryview, filename):
    print("Parsing jpg/JFIF(APP0)")
    print_basic_info(filename)


def parse_jpg_Canon_ICC_APP2(binary_file:memoryview, filename):
    print("jpg/Canon/ICC(APP2) file detected, printing basic metadata")
    print_basic_info(filename)


def parse_jpg_DQT(binary_file:memoryview, filename):
    print("jpg/DQT file detected file detected, printing basic metadata")
    print_basic_info(filename)


def parse_png(binary_file:memoryview, filename):
    print("png file detected file detected, printing basic metadata")
    print_basic_info(filename)


def parse_gif1(binary_file:memoryview, filename):
    print("gif file detected file detected, printing basic metadata")
    print_basic_info(filename)


def parse_gif2(binary_file:memoryview, filename):
    print("gif file detected file detected, printing basic metadata")
    print_basic_info(filename)


def parse_bmp(binary_file:memoryview, filename):
    print("bmp file detected file detected, printing basic metadata")
    print_basic_info(filename)

def parse_error(binary_file:memoryview, filename):
    print("File format not supported")
    sys.exit(1)


def choose_file_parser(extension:str, binary_file:memoryview, filename) -> None:
    functions = {
        '.jpg/JFIF(APP0)': parse_jpg_JFIF_APP0,
        '.jpg/Exif(APP1)': parse_jpg_Exif_APP1,
        '.jpg/Canon/ICC(APP2)': parse_jpg_Canon_ICC_APP2,
        '.jpg/DQT': parse_jpg_DQT,
        '.png':  parse_png,
        '.gif1': parse_gif1,
        '.gif2': parse_gif2,
        '.bmp':  parse_bmp,
        None:  parse_error
    }
    if extension not in functions:
        print(f"File extension ({extension}) is not supported")
        return
    functions[extension](binary_file, filename)


def get_metadata(filename):
    with open(filename, 'rb') as file:
        binary_file = memoryview(file.read()).cast('B')
        choose_file_parser(identify_type(binary_file), binary_file, filename)


if __name__ == '__main__':
    for file in FILES:
        print(f"\n--------- {file} ---------")
        get_metadata(file)
