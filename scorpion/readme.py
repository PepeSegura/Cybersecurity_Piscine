"""
    Exif format

    SOI = Start Of Image (Always 0xFFD8)
    SOS = Start Of Stream
    EOI = End Of Image (Always 0xFFD9)

    SOI Marker  | Marker                | SOS                   | Image stream  | EOI Marker    |
    FFD8        | FFXX SSSS DDDD....    | FFDA UUUU DDDD....    | IIII....      | FFD9          |

    
    Marker used by Exif is Tiff

    Tiff format

    Alignment       | TAG Mark  | Offset to first IDF   |
    "II" or "MM"    | 2A00      | 0x0000 0008           |

    "II" = Little endian
    "MM" = Big endian

    
    IDF: Image file directory

    IDF format
    
    Number of entries   | Entry1    | Entry2    | Offset to next IFD    |
    EE EE - 2 bytes     | 12 bytes  | 12 bytes  | LLLL LLLL - 4 bytes   |

    
    Entry format

    TAG number      | Data format       | Number of Components  | Data or offset to data    |
    TT TT - 2 bytes | ff ff - 2 bytes   | NNNN NNNN - 4 bytes   | DDDD DDDD - 4 bytes       |


    Data format
    1  - unsigned byte      - 1 byte
    2  - ascii strings      - 1 byte
    3  - unsigned short     - 2 byte
    4  - unsigned long      - 4 byte
    5  - unsigned rational  - 8 byte
    6  - signed byte        - 1 byte
    7  - undefined          - 1 byte
    8  - signed short       - 2 byte
    9  - signed long        - 4 byte
    10 - signed rational    - 8 byte
    11 - single float       - 4 byte
    12 - double float       - 8 byte

    Total data size = number of components * sizeof(data format)
    if (Total data size > 4 bytes)
        Data = offset to data



Exif\0\0
TIFF HEADER
    2 bytes  - byte order (II or MM)
    2 bytes  - 0x002A
    4 bytes  - offset to IFD0

IFD structure:
    2 bytes  - number of entries (N)

    N x 12 bytes entries:
        2  - Tag
        2  - Type
        4  - Count
        4  - Value OR Offset

    4 bytes - Offset to next IFD (0 if none)
 
"""