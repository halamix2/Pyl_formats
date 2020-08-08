#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import DAT, Mipmap
from glob import glob

def main():

    glo = glob('LEVEL/**/*.GFX')
    glo.sort()

    for gfx_file in glo:
        print(gfx_file)
        gfx = DAT.from_dat(gfx_file)

        if not gfx:
            print('Not a valid spr file, skip')
            continue

        output = str(Path(gfx_file).parent/Path(gfx_file).stem)+'_GFX'
        print('out', output)
        gfx.to_folder(output)

    glo_pics = glob('LEVEL/**/MAP_GFX/**')
    glo_pics.sort()
    for pic in glo_pics:
        print(pic)
        mipmap = Mipmap.from_mipmap(pic)

        if not mipmap:
            raise Exception('Not a valid mipmap file')

        output = Path(pic) #.with_suffix('.png')
        mipmap.to_png_top(output)  # only one mipmap

if __name__ == "__main__":
    main()
