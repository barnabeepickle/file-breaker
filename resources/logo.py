"""Generates a logo for this project using Pillow."""
# imports
from PIL import Image,ImageDraw,ImageFont
import os

# var
square_size=2000
rad=square_size*0.04
#rad=120 # uncomment this to override
sub_size=(square_size,square_size)
half=sub_size[0]//2
text_px=sub_size[0]*0.7
text_px=text_px//1
spacer=40
logo_size=(sub_size[0]*3,sub_size[1])
color_table={1:'#818589',
            2:'#7a7a7a',
            3:'#737373'}

# func
def add_center_text(draw,in_text):
    """Adds text to the center of an image using Pillow."""
    font=ImageFont.truetype('resources/Audiowide/Audiowide-Regular.ttf',text_px,0,'unic')
    draw.text((half,half),in_text,'#f0ffff',font,'mm')
    
def square_maker(filename,hex,s_size,s_rad,in_text=''):
    """Creates a flat color square in an image using Pillow."""
    with Image.new('RGBA',s_size,'#00000000') as square:
        draw=ImageDraw.Draw(square)
        draw.rounded_rectangle((spacer,spacer,sub_size[0]-spacer,sub_size[1]-spacer),s_rad,hex)
        if not in_text=='':
            add_center_text(draw,in_text)
        square.save(f'{filename}.png')

# code
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
    logo.save('logo_source.png')
square1.close()
square2.close()
square3.close()
x=0
for x in range(1,4):
    os.remove(f'square{x}.png')
    x+=1
del(x)