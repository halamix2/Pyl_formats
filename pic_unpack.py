#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import PIC

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the pc file")
parser.add_argument("-o", "--output", help="name of the output file")


def main():
    args = parser.parse_args()

    pic = PIC.from_pic(args.filename)

    if not pic:
        raise Exception('Not a valid spr file')

    output = Path(args.filename).with_suffix('.png')
    print(output)
    if args.output:
        output = args.output
    pic.to_png(output)

if __name__ == "__main__":
    main()
