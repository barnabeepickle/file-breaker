"""The CLI interface for file-breaker."""
# imports
import file_breaker
import argparse

# argparse parser
parser = argparse.ArgumentParser( # most of this is just taken directly from the documentation
                    prog='file-breaker-cli',
                    usage='%(prog)s [options]', # smarter code than I, now don't quote me on that
                    description='A CLI interface for breaking files into segments.',
                    epilog='"AS IS", WITHOUT WARRANTY')
# argparse arguments
parser.add_argument('input_path',type=str,help='Path to the input file.')
parser.add_argument('-b', '--break',action='store_true',help='If the input file should be split into parts.')
parser.add_argument('-e', '--extract',action='store_true',help='If the input file should be reassembled')
parser.add_argument('-s', '--size',type=int,help='Specify the size in bytes of the output file.')

