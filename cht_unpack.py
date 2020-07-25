#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import CHT


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the SPR file")
parser.add_argument("-o", "--output", help="name of the output folder")


def main():
    args = parser.parse_args()

    cht = CHT.from_cht(args.filename)

    if not cht:
        raise Exception('Not a valid cht archive')

    output = Path(args.filename).parent/Path(args.filename).stem
    if args.output:
        output = args.output
    cht.to_folder(output)

if __name__ == "__main__":
    main()
