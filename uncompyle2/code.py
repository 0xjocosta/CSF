import struct
import sys
from PIL import Image


def embed(imgFile):
    v = []
    img = Image.open(imgFile)
    width, height = img.size
    conv = img.convert('RGBA').getdata()
    print '[*] Input image size: %dx%d pixels.' % (width, height)
    max_size = width * height * 3.0 / 8 / 1024
    print '[*] Usable payload size: %.2f KB.' % max_size

    idx = 0
    displacement = 0
    password = 0
    for h in range(height):
        for w in range(width):
            if displacement < password:
                displacement = displacement + 1
                continue
            r, g, b, a = conv.getpixel((w, h))
            #if idx < len(v):
            v.append(set_bit(r, 0))
            v.append(set_bit(r, 1))
            v.append(set_bit(g, 0))
            v.append(set_bit(g, 1))
            v.append(set_bit(b, 0))
            v.append(set_bit(b, 1))

    compose(v)

def set_bit(n, i):
    mask = 1 << i
    n &= mask
    if n == 2:
        n = 1
    return n


def compose(v):
    fsize = 0
    print(v[0:8])
    for bit in v[0:8]:
        fsize = (fsize << 1) | bit
    print 'Size'
    print (fsize)

    data = ''
    for byte in range(1, (fsize +3), 1):
        char = 0
        for bit in v[byte*8: (byte + 1)*8]:
            char = (char << 1) | bit
        data = data + chr(char)

    print (data)


if __name__ == '__main__':
    embed(sys.argv[1])
