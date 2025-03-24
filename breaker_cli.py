"""The CLI interface for file-breaker."""
# imports
import file_breaker
import argparse
import pathlib

# argparse setup
parser=argparse.ArgumentParser( # most of this is just taken directly from the documentation
                    prog='file-breaker-cli',
                    usage='%(prog)s [options]', # smarter code than I, now don't quote me on that, 
                    # maybe quote me on that, this code comment has gone on long enough!
                    description='A CLI interface for breaking files into segments.',
                    epilog='"AS IS", WITHOUT WARRANTY')
parser.add_argument('input_path',
                    type=pathlib.Path,
                    help='Path to the input file.')
parser.add_argument('mode',
                    type=str,
                    help='If the input file should be broken or reassembled')
parser.add_argument('-s', '--size',
                    type=int,
                    help='Specify the size in bytes of the output file.',
                    default=1024*1024*50)
parser.add_argument('-c','-csv',
                    help='Disable the need for a CSV file (generates index on demand).',
                    action='store_true')
parser.parse_args() # TODO: implement this correctly

# code
# TODO: write the code that goes here