"""The CLI interface for file-breaker."""
# imports
import file_breaker as breaker
import argparse
import pathlib

# vars
default_size=1024*1024*50

# argparse setup
modes=['break','build','gen']
mode_key={'break':0,'build':1,'gen':2}
# setup the program/parser/wrapper
parser=argparse.ArgumentParser( # most of this is just taken directly from the documentation
                    prog='file-breaker-cli',
                    usage='%(prog)s [options]', # smarter code than I, now don't quote me on that, 
                    # maybe quote me on that, this code comment has gone on long enough!
                    description='A CLI interface for breaking files into segments.',
                    epilog='"AS IS", WITHOUT WARRANTY')
# add the arguments
parser.add_argument('input_path',
                    type=pathlib.Path,
                    help='Path to the input file.')
parser.add_argument('mode',
                    type=str,
                    choices=modes,
                    help='If the input file should be broken or reassembled')
parser.add_argument('-s', '--size',
                    type=int,
                    help='Specify the size in bytes of the output file.',
                    default=default_size)
parser.add_argument('-c','--csv',
                    help='Disable the need for a CSV file (generates index on demand).',
                    action='store_true')
# parse the arguments
path=''
parser.parse_args(args=['input_path'],namespace=path)
mode=''
parser.parse_args(args=['mode'],namespace=mode)
mode=mode_key[mode]
size=default_size
parser.parse_args(args=['-s','--size'],namespace=size)
gen_index=False
parser.parse_args(args=['-c','--csv'],namespace=gen_index)
# i don't know how to write good argparse .parse_args() code

# code
if mode==2: # part of the mode==2 additions to gen_index
    gen_index=True
if gen_index==True: # handles the -c, --csv, gen_index or mode==2 args
    overrides=breaker.index_gen(path)
    if overrides[0]==True:
        part_override=f'{path}.new'
        if mode==2:
            print(f'The new part index file has been generated with the name: {part_override}')
    if overrides[1]==True:
        tar_override=f'{path}.new'
        if mode==2:
            print(f'The new tar index file has been generated with the name: {tar_override}')
    if mode==2:
        print('The new index files have been generated correctly.')
if mode==0:
    breaker.file_break() # TODO
elif mode==1:
    breaker.file_build() # TODO