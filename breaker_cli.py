"""The CLI interface for file-breaker."""
# imports
import file_breaker
import argparse
import pathlib

# vars
default_size=1024*1024*50

# argparse setup
mode_key={'break':0,'build':1}
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
                    choices=['break','build'],
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
index_gen=False
parser.parse_args(args=['-c','--csv'],namespace=index_gen)
# i don't know how to write good argparse .parse_args() code

# code
# TODO: write the code that goes here