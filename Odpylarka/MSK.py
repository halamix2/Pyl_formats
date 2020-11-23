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
class PIC():
    def __init__(self):
        self.__width = 0
        self.__height = 0
        self.__data = b''
    
    @classmethod
    def from_pic(cls, filename: str):
        new_pic = cls()
        lines_data = []
        with open(filename, 'rb') as pic_file:
            hoh = struct.unpack("<L",pic_file.read(4))[0]
            if hoh !=0:
                print('This is usually set to 0, beware, this might not be a PIC file')
            new_pic.__height = struct.unpack("<L",pic_file.read(4))[0]

            line = 0

            lines_data = [b''] * new_pic.__height
            file_size = os.fstat(pic_file.fileno()).st_size
            while pic_file.tell() < file_size and line < new_pic.__height:
                blocks = struct.unpack("<L",pic_file.read(4))[0]

                for block in range(blocks):
                    if pic_file.tell() < file_size:
                        width_data = struct.unpack("<L",pic_file.read(4))[0]
                        starting_position = struct.unpack("<L",pic_file.read(4))[0]
                        block_data = pic_file.read(width_data * 2)

                        lines_data[line] += b''.join([b'\x00\x00'] * (starting_position - int(len(lines_data[line]) /2)))
                        lines_data[line] += block_data
                        if(pic_file.tell() % 4 != 0):
                            # TODO I hope this will work with ther files as well
                            ech = pic_file.read(4 - (pic_file.tell() % 4))
                            print('skipping bytes')
                    else:
                        print('something\'s wrong, there should be a block here, but I only see end of the file')
                        break
                line += 1

        new_pic.__width = int(len(max(lines_data, key=len)) / 2)
        if new_pic.__width == 0:
            new_pic.__width = 1

        for line in lines_data:
            new_pic.__data += line
            new_pic.__data += b''.join([b'\x00\x00'] * (new_pic.__width - int(len(line) / 2)))

        
        if new_pic.check():
            return new_pic
    
    @classmethod
    def from_png(cls, filename: str):
        new_pic = cls()
        image = Image.open(filename).convert("RGBA")
        new_pic.__width = image.width
        new_pic.__height = image.height

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

            new_pic.__data += pixel_16.to_bytes(2, 'little')


        if len(new_pic.__data) == 0:
            raise Exception('SPR data cannot be empty!')
        return new_pic
   
    
    def to_pc(self, filename: str):
        with open(filename, 'wb') as pic_file:
            pic_file.write(self.__width.to_bytes(4, 'little'))
            pic_file.write(self.__height.to_bytes(4, 'little'))
            pic_file.write(self.__data)
        pass
    
    def to_png(self, filename: str):
        # print('saving to', filename)
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
        
    def get_width(self):
        return self.__width
        
    def get_height(self):
        return self.__height
        
    def get_data(self):
        return self.__data
        
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
