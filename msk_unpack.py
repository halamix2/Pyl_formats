#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import MSK

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the msk file")
parser.add_argument("-o", "--output", help="name of the output file")


def main():
    args = parser.parse_args()

    msk = MSK.from_pic(args.filename)

    if not msk:
        raise Exception('Not a valid msk file?')

    output = Path(args.filename).with_suffix('.png')
    print(output)
    if args.output:
        output = args.output
    msk.to_png(output)

if __name__ == "__main__":
    main()
