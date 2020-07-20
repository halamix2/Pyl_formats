#!/usr/bin/python3 
# coding=utf-8

class FileEntry:
    def __init__(self, filename: str, data: bytes):
        # yeah, I know, missing check if the name is <= 13 chars
        self.filename = filename
        self.data = data
    
    def __str__(self) -> str:
        return self.filename+": "+str(self.size)+' bytes'
    
    def __repr__(self) -> str:
        """For array, print just filename"""
        return '\n"'+self.filename+'"'

    def __lt__(self, other):
        return self.filename < other.filename
    
    @property
    def size(self):
        return len(self.__data)

    @property
    def filename_padding(self):
        return b''.join([b'\x00'] * (22-len(self.filename)))
