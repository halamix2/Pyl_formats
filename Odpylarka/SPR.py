#!/usr/bin/python3 
# coding=utf-8

import os
import sys

#import pandas as pd
#import numpy as np

# files
import pathlib
#from glob import glob

from PIL import Image # type: ignore

#binary
import struct

#TODO check if size is at least 1x1
class SPR():
    def __init__(self):
        self.__width = 0
        self.__height = 0
        self.__data = b''
    
    @classmethod
    def from_spr(cls, filename: str):
        new_spr = cls()
        with open(filename, 'rb') as pc_file:
            new_spr.__width = struct.unpack("<L",pc_file.read(4))[0]
            new_spr.__height = struct.unpack("<L",pc_file.read(4))[0]
            new_spr.__data = pc_file.read()
            
        if new_spr.check():
            print('ok')
            return new_spr
    
    @classmethod
    def from_png(cls, filename: str):
        new_spr = cls()
        image = Image.open(filename).convert("RGBA")
        new_spr.__width = image.width
        new_spr.__height = image.height

        pixels = list(image.getdata())
        for r, g, b, alpha in pixels:
            pixel_16 = 0

            # one byte alpha
            alpha = round(alpha >= 128)
            pixel_16 += alpha << 15

            # convert 0-255 to 0-31
            r = round(31*(r/255))
            pixel_16 += r << 10

            g = round(31*(g/255))
            pixel_16 += g << 5

            b = round(31*(b/255))
            pixel_16 += b

            new_spr.__data += pixel_16.to_bytes(2, 'little')


        if len(new_spr.__data) == 0:
            raise Exception('SPR data cannot be empty!')
        return new_spr
   
    
    def to_pc(self, filename: str):
        with open(filename, 'wb') as pc_file:
            pc_file.write(self.__width.to_bytes(4, 'little'))
            pc_file.write(self.__height.to_bytes(4, 'little'))
            pc_file.write(self.__data)
        pass
    
    def to_png(self, filename: str):
        print('saving to', filename)
        image = Image.new('RGBA', (self.__width, self.__height))
        #Image.new('RGBA', (data['width'], data['height']))
        image.putdata(self.__convert_color(self.__data))
        image.save(filename, 'PNG')
    
    def check(self) -> bool:
    
        try:
            assert self.__width > 0, 'width <= 0'
            assert self.__height > 0, 'height <= 0'

        except AssertionError as error:
            print('assertion error:', error)
            return False
           
        return True

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
