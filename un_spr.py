#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import SPR
from glob import glob

def main():
    glo = glob('out/**/*.SPR')

    glo.sort()

    for spr_file in glo:
        print(spr_file)
        spr = SPR.from_spr(spr_file)

        if not spr:
            print('Not a valid pic file, skip')
            continue

        output = Path(spr_file).with_suffix('.png')
        spr.to_png(output)

if __name__ == "__main__":
    main()
