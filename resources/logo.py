"""Generates a logo for this project using Pillow."""
# imports
import PIL
from PIL import Image,ImageDraw,ImageFont
import os

# var
rad=60
sub_size=(1000,1000)
half=sub_size[0]//2
text_px=sub_size[0]*0.7
text_px=text_px//1
logo_size=(sub_size[0]*3,sub_size[1])

# func
def add_corners(im, rad): # stolen from stackoverflow 11287402 # work smarter not harder
    """Adds rounded corners to a square image using Pillow"""
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

def add_center_text(im,in_text): # not stolen, written from scratch
    """Adds text to the center of an image using Pillow."""
    draw=ImageDraw.Draw(im)
    font=ImageFont.truetype('resources/Audiowide/Audiowide-Regular.ttf',text_px,0,'unic')
    draw.text((half,half),in_text,'#f0ffff',font,'mm')
    return im
    
def square_maker(filename,hex,s_size,s_rad,in_text=''):
    """Creates a flat color square in an image using Pillow."""
    with Image.new('RGBA',s_size,hex) as square:
        square=add_corners(square,s_rad)
        if not in_text=='':
            square=add_center_text(square,in_text)
        square.save(f'{filename}.png')

# code
color_table={1:'#818589',
            2:'#7a7a7a',
            3:'#737373'}
x=1
for x in range(1,4):
    square_maker(f'square{x}',color_table[x],sub_size,rad,f'{x}')
    x+=1
square1=Image.open('square1.png')
square2=Image.open('square2.png')
square3=Image.open('square3.png')
with Image.new('RGBA',logo_size) as logo:
    logo.paste(square1,(0,0))
    logo.paste(square2,(sub_size[0],0))
    logo.paste(square3,(sub_size[0]*2,0))
    logo.save('logo.png')
square1.close()
square2.close()
square3.close()
x=0
for x in range(1,4):
    os.remove(f'square{x}.png')
    x+=1
del(x)