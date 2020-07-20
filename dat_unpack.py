#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import DAT


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the SPR file")
parser.add_argument("-o", "--output", help="name of the output folder")


def main():
    args = parser.parse_args()

    dat = DAT.from_dat(args.filename)

    if not dat:
        raise Exception('Not a valid dat archive')

    output = Path(args.filename).parent/Path(args.filename).stem
    if args.output:
        output = args.output
    dat.to_folder(output)

if __name__ == "__main__":
    main()
