#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import Mipmap

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the mipmap file")
parser.add_argument("-o", "--output", help="prefix of the output file")


def main():
    args = parser.parse_args()

    mipmap = Mipmap.from_mipmap(args.filename)

    if not mipmap:
        raise Exception('Not a valid mipmap file')

    output = Path(args.filename) #.with_suffix('.png')
    print(output)
    if args.output:
        output = args.output
    mipmap.to_pngs(output)

if __name__ == "__main__":
    main()
