import numpy
import sys
from time import time
from math import sqrt, cos
import argparse

from pal import stringify, pal_str

def write_pgm(data, fname):
  f = open(fname, "wb")
  f.write("P5\r\n".encode('charmap'))
  f.write(f"{width} {height}\r\n".encode('charmap'))
  f.write("65535\r\n".encode('charmap'))
  data = numpy.array(data, dtype='int16')
  f.write(data.tobytes())
  f.close()

def circle(x, y):
    return x**2 + y**2

def div(x, y):
    if y == 0:
        return 12 # first non palindrome integer
    else:
        return x / y

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fractals of palindrome numbers", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f',
                        '--function',
                        type=str,
                        default="circle",
                        dest="function",
                        help='circle or div')
    parser.add_argument('-wh',
                        '--width', 
                        help="width", 
                        type=int, 
                        default=500,
                        dest="width")
    parser.add_argument('-hh',
                        '--height', 
                        help="height", 
                        type=int, 
                        default=500,
                        dest="height")
    parser.add_argument('-s',
                        '--scale',
                        help="integer between 0 and computing power",
                        type=int,
                        default=0,
                        dest="scale")

    args = parser.parse_args()
    height = args.height
    width = args.width
    scale = args.scale

    t = time()
    max_count = 0
    max_x = 0
    min_x = 0

    data = []
    for h in range(int(height/2), int(-height/2), -1):
        for w in range(int(-width/2), int(width/2)):
            x = round(w/10**scale, scale)
            y = round(h/10**scale, scale)
    
            max_x = max(max_x, x)
            min_x = min(min_x, x)

            if args.function == 'circle':
                z = circle(x, y)
            elif args.function == 'div':
                z = div(x, y)
            else:
                raise ValueError

            s = stringify(z)
            if pal_str(s):
                l = len(s)
                max_count = max(max_count, l)
                data.append(l)
            else:
                data.append(0)

    newdata = []
    for n in data:
        if n > 0:
            newdata.append(n + (65535 - max_count))
        else:
            newdata.append(0)

    data = newdata 

    write_pgm(data, f"pal_{args.function}_{scale}_{width}_{height}.pgm")
    sys.stderr.write("elapsed time: %.1f seconds\r\n" % (time()-t))
    sys.stderr.write("largest count: %d\r\n" % max_count)
    sys.stderr.write("max x : %d\r\n" % max_x)
    sys.stderr.write("min x : %d\r\n" % min_x)
