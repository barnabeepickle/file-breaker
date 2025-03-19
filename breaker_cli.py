"""The CLI interface for file-breaker."""
# imports
import file_breaker
import argparse

parser = argparse.ArgumentParser( # most of this is just taken directly from the documentation
                    prog='file-breaker-cli',
                    usage='%(prog)s [options]', # smarter code than I
                    description='A CLI interface for breaking files into segments.',
                    epilog='"AS IS", WITHOUT WARRANTY')
parser.add_argument('input_path')
parser.add_argument('-b', '--break',action='store_true')
parser.add_argument('-e', '--extract',action='store_true')
parser.add_argument('-s', '--size')
