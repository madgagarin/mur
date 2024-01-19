from math import ceil
from zlib import crc32, compress
from struct import pack
from itertools import chain

import numpy as np


def make_grid(x_size: int, y_size: int) -> tuple[list[bool], ...]:
    return tuple([False] * x_size for _ in range(y_size))


def list_of_bool_to_rgba(list_of_bool: list[bool]) -> iter:
    return (b"\x00\x00\x00\xff" if x else b"\xff\xff\xff\xff" for x in list_of_bool)


def png_pack(png_tag: bytes, data: bytes) -> bytes:
    chunk_head = png_tag + data
    return (
        pack("!I", len(data)) + chunk_head + pack("!I", 0xFFFFFFFF & crc32(chunk_head))
    )


def make_1bit_png(bool_buffer, width, height, m2):
    raw_data = []
    width1 = 2

    ncols, rembits = divmod(width, 8)
    if rembits > 0:
        ncols += 1
    print(ncols)
    print(rembits)

    b = np.zeros((height, ncols), dtype=np.uint8)
    print(b)
    for row in range(height):
        bcol = 0
        pos = 8
        for col in range(width):
            val = (2**1 - 1) & m2[row][col] ###
            print(val)
            pos -= 1
            if pos < 0:
                bcol += 1
                pos = 8 - 1
            b[row, bcol] |= val << pos
    print(b)

    for y in range(height):
        cc = bool_buffer[y * width1 : (y + 1) * width1]
        print(cc)
        raw_data.append(b"\x00" + bytes(cc))
    print(list(raw_data))
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_pack(b"IHDR", pack("!2I5B", width, height, 1, 0, 0, 0, 0)),
            png_pack(b"IDAT", compress(b"".join(raw_data), 9)),
            png_pack(b"IEND", b""),
        ]
    )


def make_rgba_png(rgba_buffer: iter, width: int, height: int) -> bytes:
    width_4 = width * 4
    raw_data = (
        b"\x00" + bytes(rgba_buffer[y * width_4 : (y + 1) * width_4])
        for y in range(height)
    )
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_pack(b"IHDR", pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
            png_pack(b"IDAT", compress(b"".join(raw_data), 9)),
            png_pack(b"IEND", b""),
        ]
    )


size_x, size_y = 10, 10
now_x, now_y = 7, 2
direction = (True, True)

matrix = make_grid(size_x, size_y)
black_count = 0

# while 0 <= now_x < size_x and 0 <= now_y < size_y:
#     if direction == (True, True):
#         # Up
#         if matrix[now_x][now_y]:
#             now_x -= 1
#             direction = (False, False)
#         else:
#             now_x += 1
#             direction = (False, True)
#     elif direction == (True, False):
#         # Down
#         if matrix[now_x][now_y]:
#             now_x += 1
#             direction = (False, True)
#         else:
#             now_x -= 1
#             direction = (False, False)
#     elif direction == (False, True):
#         # right
#         if matrix[now_x][now_y]:
#             now_y += 1
#             direction = (True, True)
#         else:
#             now_y -= 1
#             direction = (True, False)
#     elif direction == (False, False):
#         # left
#         if matrix[now_x][now_y]:
#             now_y -= 1
#             direction = (True, False)
#         else:
#             now_y += 1
#             direction = (True, True)
#     else:
#         print("Wrong direction")
#     if matrix[now_x][now_y]:
#         matrix[now_x][now_y] = False
#         black_count -= 1
#     else:
#         matrix[now_x][now_y] = True
#         black_count += 1


for f in range(min(size_x, size_y)):
    matrix[f][f] = True
print(matrix)

def listmerge(lstlst):
    all = []
    for lst in lstlst:
        all.extend(lst)
    return all


bool_list = listmerge(reversed(matrix))
rgba_int_list = tuple(
    chain.from_iterable(list_of_bool_to_rgba(chain.from_iterable(reversed(matrix))))
)
print(bool_list)

with open("a.png", "wb") as fp:
    fp.write(make_rgba_png(rgba_int_list, size_x, size_y))

with open("b.png", "wb") as fp:
    fp.write(make_1bit_png(bool_list, size_x, size_y, matrix))
