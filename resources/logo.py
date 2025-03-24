"""Generates a logo for this project using Pillow."""
# imports
import PIL
from PIL import Image,ImageDraw,ImageFont
import os

# var
rad=60
sub_size=(1000,1000)
half=sub_size[0]//2
logo_size=(sub_size[0]*3,sub_size[1])

# func
def add_corners(im, rad): # stolen from stackoverflow 11287402 # work smarter not harder
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
    x,y=im.size
    font=ImageFont.truetype('resources/Audiowide/Audiowide-Regular.ttf',half,0,'unic')
    txt=ImageDraw.ImageDraw.text((x,y),in_text,'#f0ffff',font,'mm',4,'Center','rtl','None','en',0,'#f0ffff',False,12)
    im.paste(txt,(0,0))
    return im
    
def square_maker(filename,hex,s_size,s_rad,in_text=''):
    with Image.new('RGBA',s_size,hex) as square:
        square=add_corners(square,s_rad)
        if not in_text=='':
            square=add_center_text(square,in_text)
        square.save(f'{filename}.png')

# code
square_maker('square1','#818589',sub_size,rad,'')
square_maker('square2','#7a7a7a',sub_size,rad,'')
square_maker('square3','#737373',sub_size,rad,'')
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
os.remove('square1.png')
os.remove('square2.png')
os.remove('square3.png')