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

# var
rad=50
size=(1000,1000)
logo_size=(size[0]*3,size[1])
# code
with Image.new('RGBA',size,'#818589') as square:
    square=add_corners(square,rad)
    square.save('square1.png')
with Image.new('RGBA',size,'#7a7a7a') as square:
    square=add_corners(square,rad)
    square.save('square2.png')
with Image.new('RGBA',size,'#737373') as square:
    square=add_corners(square,rad)
    square.save('square3.png')
square1=Image.open('square1.png')
square2=Image.open('square2.png')
square3=Image.open('square3.png')
with Image.new('RGBA',logo_size) as logo:
    logo.paste(square1,(0,0))
    logo.paste(square2,(size[0],0))
    logo.paste(square3,(size[0]*2,0))
    logo.save('logo.png')
square1.close()
square2.close()
square3.close()
os.remove('square1.png')
os.remove('square2.png')
os.remove('square3.png')