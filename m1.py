from zlib import crc32, compress
from struct import pack
from itertools import chain


def make_grid(x_size: int, y_size: int) -> list[list[bool]]:
    return [[False] * x_size for _ in range(y_size)]


def list_of_bool_to_rgba(list_of_bool: list[bool]) -> iter:
    return ([0, 0, 0, 255] if x else [255, 255, 255, 255] for x in list_of_bool)


def png_pack(png_tag: bytes, data: bytes) -> bytes:
    chunk_head = png_tag + data
    return pack("!I", len(data)) + chunk_head + pack("!I", 0xFFFFFFFF & crc32(chunk_head))


def rgba_png(buffer: iter, width: int, height: int) -> bytes:
    width_byte_4 = width * 4
    raw_data = bytearray()
    for y in range(height):
        raw_data.extend(b'\x00')
        raw_data.extend(buffer[y * width_byte_4:(y + 1) * width_byte_4])

    return b"".join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', compress(bytes(raw_data), 9)),
        png_pack(b'IEND', b'')])


size = 10, 6
start_position = 5, 5

matrix = make_grid(*size)
matrix[1][1] = True
matrix[0][0] = True

int_list = list(chain.from_iterable(list_of_bool_to_rgba(chain.from_iterable(matrix))))

with open('a.png', 'wb') as fp:
    fp.write(rgba_png(int_list, size[0], size[1]))
