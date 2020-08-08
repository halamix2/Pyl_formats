#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import PIC
from glob import glob

def main():
    glo = glob('out/**/*.PIC')

    glo.sort()

    for pic_file in glo:
        print('opening', pic_file)
        pic = PIC.from_pic(pic_file)

        if not pic:
            print('Not a valid pic file, skip')
            continue

        output = Path(pic_file).with_suffix('.png')
        print('saving')
        pic.to_png(output)

if __name__ == "__main__":
    main()
