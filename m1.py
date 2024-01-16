import zlib, struct
from itertools import chain

size = 10, 6
start_position = 5, 5


def make_grid(x_size, y_size):
    return [[False] * x_size for _ in range(y_size)]


m = make_grid(*size)
m[1][1] = True
m[0][0] = True


def list_of_bool_to_argb(list_of_bool):
    return [[0, 0, 0, 255] if x else [255, 255, 255, 255] for x in list_of_bool]


ar = list(chain.from_iterable(list_of_bool_to_argb(chain.from_iterable(m))))


def png_pack(png_tag, data):
    chunk_head = png_tag + data
    return struct.pack("!I", len(data)) + chunk_head + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))


def write_rgba_png(buf, width, height):
    width_byte_4 = width * 4
    raw_data = bytearray()
    for y in range(height):
        raw_data.extend(b'\x00')
        raw_data.extend(buf[y * width_byte_4:(y + 1) * width_byte_4])

    return b"".join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(bytes(raw_data), 9)),
        png_pack(b'IEND', b'')])


with open('a.png', 'wb') as fp:
    fp.write(write_rgba_png(ar, size[0], size[1]))
