#!/usr/bin/python3 
# coding=utf-8

import os
import sys

# files
from pathlib import Path
# from glob import glob

from typing import List, Dict, Optional

#binary
import struct
from Odpylarka.FileEntry import FileEntry

import io
from PIL import Image # type: ignore

class CHT():
    def __init__(self):
        # TODO make class out of this or at least add there aren't two files with the same name (case insensitive)
        self.files = []

    @classmethod
    def from_cht(cls, filename: str):
        new_cht = cls()
        with open(filename, 'rb') as cht_file:
            files_count = struct.unpack("<L", cht_file.read(4))[0]
            # read files

            for i in range(files_count):
                # jump back to hash table
                cht_file.seek(0x4 + i*0xD)
                # read filename
                filename = cht_file.read(9)
                terminator = filename.index(b'\x00')
                filename = filename[:terminator].decode('ascii')
                offset = struct.unpack("<L", cht_file.read(4))[0]

                cht_file.seek(offset)
                size = struct.unpack("<L", cht_file.read(4))[0]
                data = cht_file.read(size * size)
                
                image = Image.new('RGBA', (size, size))
                image.putdata(new_cht.__convert_color(data))

                imgByteArr = io.BytesIO()
                image.save(imgByteArr, 'PNG')
                # cht_file.seek(file_offset)
                # data = cht_file.read(file_size)

                new_cht.files.append(FileEntry(filename+'.png', imgByteArr.getvalue())) #TODO make it more classy, for now you force PNG format

        return new_cht

    def to_folder(self, folder):
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        for i, file_entry in enumerate(self.files, start=0):
            if file_entry:
                tmp_filename = Path(path/file_entry.filename.replace('\\', '/'))
                tmp_filename.parent.mkdir(parents=True, exist_ok=True)
                with open(tmp_filename, 'wb') as tmp_file:
                    tmp_file.write(file_entry.data)


    @staticmethod
    def __convert_color(data):
        pixels = []
        if len(data) % 2 != 0:
            sys.exit('wrong number of data for color converter')

        #each pixel is stored on 2 bytes, in A1 R5 G5 B5  format
        pixels_data = memoryview(data).cast('H')
        for pixel in pixels_data:
            # 5 bits means 2^5-1 = 31
            red =  round((pixel >> 10 &   31) * (255/31))
            green = round((pixel >> 5 &  31) * (255/31))
            blue = round( (pixel &  31) * (255/31))
            alpha = round((pixel >15 & 1) * 255)
            
            pixels.append((red, green, blue, alpha))
        return pixels