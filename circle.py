import numpy
import sys
from time import time
from math import sqrt, cos, log
import argparse

DELTA = 0.01


def write_pgm(data, fname):
    f = open(fname, "wb")
    f.write("P5\r\n".encode('charmap'))
    f.write(f"{width} {height}\r\n".encode('charmap'))
    f.write("65535\r\n".encode('charmap'))
    data = numpy.array(data, dtype='int16')
    f.write(data.tobytes())
    f.close()

def interp(old_value, old_min, old_max, new_min, new_max):
    return ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fractals of palindrome numbers", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n',
                        '--n',
                        type=int,
                        default="1",
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
                        type=float,
                        default=-1,
                        dest="start")
    parser.add_argument('-end',
                        '--end',
                        help="end",
                        type=float,
                        default=1,
                        dest="end")


    args = parser.parse_args()
    height = args.height
    width = args.width
    scale = args.scale

    t = time()

    data = []
    minh = int(-height/2)
    maxh = int(height/2)
    minw = int(-width/2)
    maxw = int(width/2)
    
    centers = {(0,0): 1}

    n = args.n
    for i in range(0, n):
        tmp_centers = {}
        for c in centers:
            minx = c[0] + (-args.c/scale**i)
            maxx = c[0] + (args.c/scale**i)
            miny = c[1] + (-args.c/scale**i)
            maxy = c[1] + (args.c/scale**i)
            for x in numpy.linspace(minx-1, maxx+1, 100):
                for y in numpy.linspace(miny-1, maxy+1, 100):
                    #print(f'{x} {y}')
                    #print(abs((x-c[0])**2 + (y-c[1])**2 - args.c/scale**i))
                    if (x-c[0])**2 + (y-c[1])**2 - ((args.c/scale**i)/2)**2 < DELTA:
                        tmp_centers[(x, y)] = 1
        centers = tmp_centers

    #print(centers)

    newcenters = {}
    for c in centers:
        newcenters[(int(interp(c[0], -args.c, args.c, minw, maxw)), int(interp(c[1], -args.c, args.c, minh, maxh)))] = 1 
    centers = newcenters

    for h in range(minh, maxh):
        for w in range(minw, maxw):
            if (w, h) in centers:
                data.append(centers[(w, h)])
            else:
                data.append(0)

    newdata = []
    for n in data:
        if n > 0:
            newdata.append(n + (65535 - 1))
        else:
            newdata.append(0)

    data = newdata 

    write_pgm(data, f"circle_{args.n}_{scale}_{width}_{height}.pgm")
    sys.stderr.write("elapsed time: %.1f seconds\r\n" % (time()-t))
