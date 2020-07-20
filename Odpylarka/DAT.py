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

class DAT():
    def __init__(self):
        # TODO make class out of this or at least add there aren't two files with the same name (case insensitive)
        self.files = []

    @classmethod
    def from_dat(cls, filename: str):
        new_dat = cls()
        with open(filename, 'rb') as dat_file:
            magic = dat_file.read(4) # magic
            if magic != b'COLL':
                return None
            data_offset = struct.unpack("<L", dat_file.read(4))[0]
            files_count = struct.unpack("<L", dat_file.read(4))[0]
            # read files

            for i in range(files_count):
                # jump back to hash table
                dat_file.seek(0x10 + i*0x16)
                # read filename
                filename = dat_file.read(14)
                terminator = filename.index(b'\x00')
                filename = filename[:terminator].decode('ascii')
                file_size, file_offset =  struct.unpack("<LL", dat_file.read(8))
                dat_file.seek(file_offset)
                data = dat_file.read(file_size)

                new_dat.files.append(FileEntry(filename, data))

        return new_dat

    def to_folder(self, folder):
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        for i, file_entry in enumerate(self.files, start=0):
            if file_entry:
                tmp_filename = Path(path/file_entry.filename.replace('\\', '/'))
                tmp_filename.parent.mkdir(parents=True, exist_ok=True)
                with open(tmp_filename, 'wb') as tmp_file:
                    tmp_file.write(file_entry.data)
