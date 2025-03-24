"""Generates a logo for this project using Pillow."""
# imports
import PIL
from PIL import Image,ImageDraw
import os

# func
def add_corners(im, rad): # stolen from stackoverflow 11287402
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def merge(im1: Image.Image, im2: Image.Image) -> Image.Image: # stolen from the pillow documentation
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    return im

# code
with Image.new('RGBA',(256,256),'#818589') as square:
    square=add_corners(square,100)
    square.save('square1.png')
with Image.new('RGBA',(256,256),'#808080') as square:
    square=add_corners(square,100)
    square.save('square2.png')
with Image.new('RGBA',(256,256),'#BEBEBE') as square:
    square=add_corners(square,100)
    square.save('square3.png')
square1=Image.open('square1.png')
square2=Image.open('square2.png')
square3=Image.open('square3.png')
squares=merge(square1,square2)
squares=merge(squares,square3)
with Image.new('RGBA',(768,256)) as logo:
    squares=logo
    squares.save('logo.png')
square1.close()
square2.close()
square3.close()
os.remove('square1.png')
os.remove('square2.png')
os.remove('square3.png')