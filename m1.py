size = 10, 6
start_position = 5, 5
import zlib, struct

def make_grid(x_size, y_size):
    row = [False for _ in range(x_size)]
    return tuple(row.copy() for _ in range(y_size))


m = make_grid(*size)
m[1][1] = True
m[0][0] = True
a = []

import math, struct

mult4 = lambda n: int(math.ceil(n / 4)) * 4
mult8 = lambda n: int(math.ceil(n / 8)) * 8
lh = lambda n: struct.pack("<h", n)
li = lambda n: struct.pack("<i", n)


def list_of_bool_to_int(list_of_bool: list[bool]) -> int:
    return int(''.join(['1' if x else '0' for x in list_of_bool]), 2)


def list_merge(list_of_list: (list[list], tuple[list])) -> list:
    all = []
    for lst in list_of_list:
        all.extend(lst)
    return all


def cut_list(big_list: list[bool], n: int) -> list[list]:
    return [big_list[i:i + n] for i in range(0, len(big_list), n)]


# m = cut_list(list_merge(m), 8)
# if (m0 := len(m[-1])) < size[0]:
#     m[-1].extend(False for _ in range(size[0] - m0))
#
# print(m[0])

smile = []
for dd in m:
    smile.append(list_of_bool_to_int(dd))


def bmp(rows, w, h):
    wB = int(mult8(w) / 8)
    s, pad = li(mult4(wB) * h + 0x20), [0] * (mult4(wB) - wB)
    return (b"BM" + s + b"\x00\x00\x00\x00\x20\x00\x00\x00\x0C\x00\x00\x00" +
            lh(w) + lh(h) + b"\x01\x00\x01\x00\xff\xff\xff\x00\x00\x00" +
            b"".join([bytes([row] + pad) for row in reversed(rows)]))


with open('a.bmp', 'wb') as fp:
    fp.write(bmp(smile, 10, 6))


def write_png(buf, width, height):
    width_byte_4 = width * 4
    raw_data = b"".join(b'\x00' + buf[span:span + width_byte_4] for span in range((height - 1) * width * 4, -1, - width_byte_4))
    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return struct.pack("!I", len(data)) + chunk_head + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
    return b"".join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])
