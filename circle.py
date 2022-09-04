import numpy
import sys
from time import time
from math import sqrt, cos, log
import argparse


def write_pgm(data, fname):
  f = open(fname, "wb")
  f.write("P5\r\n".encode('charmap'))
  f.write(f"{width} {height}\r\n".encode('charmap'))
  f.write("65535\r\n".encode('charmap'))
  data = numpy.array(data, dtype='int16')
  f.write(data.tobytes())
  f.close()

def is_on_circle(x, y, n, c, scale):
    if n < 0:
        return True
    return is_on_circle(x-(c/scale), y-(c/scale**n), n-1, c, scale**n)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fractals of palindrome numbers", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n',
                        '--n',
                        type=int,
                        default="3",
                        dest="n",
                        help='n')
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
    parser.add_argument('-c'
                        '--c',
                        help="c",
                        type=int,
                        default=1,
                        dest="c")
    parser.add_argument('-s',
                        '--scale',
                        help="integer between 0 and computing power",
                        type=int,
                        default=10,
                        dest="scale")
    parser.add_argument('-start',
                        '--start',
                        help="start",
                        type=int,
                        default=-1,
                        dest="start")
    parser.add_argument('-end',
                        '--end',
                        help="end",
                        type=int,
                        default=1,
                        dest="end")


    args = parser.parse_args()
    height = args.height
    width = args.width
    scale = args.scale

    t = time()
    max_count = 0
    max_x = 0
    min_x = 0

    data = []
    minh = int(-height/2)
    maxh = int(height/2)
    minw = int(-width/2)
    maxw = int(width/2)
    
    for h in range(minh, maxh):
        for w in range(minw, maxw):
            x = numpy.interp(w, [minw, maxw], [args.start, args.end]) 
            y = numpy.interp(h, [minh, maxh], [args.start, args.end]) 
            if is_on_circle(x, y, args.n, args.c, args.scale):
                data.append(1)
                max_count += 1
            else:
                data.append(0)

    newdata = []
    for n in data:
        if n > 0:
            newdata.append(n + (65535 - max_count))
        else:
            newdata.append(0)

    data = newdata 

    write_pgm(data, f"circle_{scale}_{width}_{height}.pgm")
    sys.stderr.write("elapsed time: %.1f seconds\r\n" % (time()-t))
    sys.stderr.write("largest count: %d\r\n" % max_count)
    sys.stderr.write("max x : %d\r\n" % max_x)
    sys.stderr.write("min x : %d\r\n" % min_x)
