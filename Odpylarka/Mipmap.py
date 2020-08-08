#!/usr/bin/python3 
# coding=utf-8

from pathlib import Path

import struct
from PIL import Image


class Mipmap():

    def __init__(self):
        pass

    @classmethod
    def from_mipmap(cls, filename: str):
        new_mipmap = cls()
        with open(filename, 'rb') as mipmap_file:
            new_mipmap.__width_0 = struct.unpack("<L",mipmap_file.read(4))[0]
            new_mipmap.__height_0 = struct.unpack("<L",mipmap_file.read(4))[0]

            # TODO this is ugly, there are always 4 mipmaps
            # check original size if it's < 8px
            new_mipmap.__width_1 =  int(new_mipmap.__width_0 / 2)
            new_mipmap.__height_1 = int(new_mipmap.__height_0 / 2)

            new_mipmap.__width_2 =  int(new_mipmap.__width_0 / 4)
            new_mipmap.__height_2 = int(new_mipmap.__height_0 / 4)

            new_mipmap.__width_3 =  int(new_mipmap.__width_0 / 8)
            new_mipmap.__height_3 = int(new_mipmap.__height_0 / 8)

            new_mipmap._image_0 = mipmap_file.read(new_mipmap.__width_0 * new_mipmap.__height_0 * 2)
            new_mipmap._image_1 = mipmap_file.read(new_mipmap.__width_1 * new_mipmap.__height_1 * 2)
            new_mipmap._image_2 = mipmap_file.read(new_mipmap.__width_2 * new_mipmap.__height_2 * 2)
            new_mipmap._image_3 = mipmap_file.read(new_mipmap.__width_3 * new_mipmap.__height_3 * 2)
            
        return new_mipmap
    
    def to_png_top(self, name):
        filename_0 = Path(str(name)+'_0.png')
        Mipmap.__to_png(self._image_0, filename_0, self.__width_0, self.__height_0)


    def to_pngs(self, name):
        print("out to {}".format(name))

        filename_0 = Path(str(name)+'_0.png')
        Mipmap.__to_png(self._image_0, filename_0, self.__width_0, self.__height_0)

        filename_1 = Path(str(name)+'_1.png')
        Mipmap.__to_png(self._image_1, filename_1, self.__width_1, self.__height_1)

        filename_2 = Path(str(name)+'_2.png')
        Mipmap.__to_png(self._image_2, filename_2, self.__width_2, self.__height_2)

        filename_3 = Path(str(name)+'_3.png')
        Mipmap.__to_png(self._image_3, filename_3, self.__width_3, self.__height_3)

    @staticmethod
    def __to_png(data, filename: str, width: int, height: int):
        image = Image.new('RGBA', (width, height))
        #Image.new('RGBA', (data['width'], data['height']))
        image.putdata(Mipmap.__convert_color(data))
        image.save(filename, 'PNG')


    # TODO move to own class common to all images
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