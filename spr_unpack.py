#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import SPR

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the pc file")
parser.add_argument("-o", "--output", help="name of the output file")


def main():
    args = parser.parse_args()

    spr = SPR.from_spr(args.filename)

    if not spr:
        raise Exception('Not a valid spr file')

    output = Path(args.filename).with_suffix('.png')
    print(output)
    if args.output:
        output = args.output
    spr.to_png(output)

if __name__ == "__main__":
    main()
