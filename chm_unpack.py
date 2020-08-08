#!/usr/bin/python3 
# coding=utf-8

import argparse
# import sys
from pathlib import Path

from Odpylarka import CHM


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of the SPR file")
parser.add_argument("-o", "--output", help="name of the output folder")


def main():
    args = parser.parse_args()

    chm = CHM.from_chm(args.filename)

    if not chm:
        raise Exception('Not a valid chm archive')

    output = Path(args.filename).parent/Path(args.filename).stem
    if args.output:
        output = args.output
    chm.to_folder(output)

if __name__ == "__main__":
    main()
