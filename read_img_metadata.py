#!/bin/python
import os
import sys
from PIL import Image, PngImagePlugin

image_file_name = sys.argv[1]

def get_info_on_var(var):
    print(im, type(var))

im = Image.open(image_file_name)
im.load()  # Needed only for .png EXIF data (see citation above)
get_info_on_var(im)
get_info_on_var(im.info)
print(im.info)

## modify image metadata
info = PngImagePlugin.PngInfo()
info.add_text("text", "This is the text I stored in a png")

output_filename = sys.argv[2]
im = Image.open(image_file_name)
im.save(output_filename, "PNG", pnginfo=info)

im3 = Image.open(output_filename)

print(im3.text["text"])