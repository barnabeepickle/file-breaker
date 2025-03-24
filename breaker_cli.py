"""The CLI interface for file_breaker using typer."""
# imports
import file_breaker as breaker
import typer
from typing_extensions import Annotated

# this code is actually okay, could be better
# (still made in like a half a week with a rewrite part way through)

# some vars
default_size=1024*1024*50
app=typer.Typer()

# func
@app.command(help='Generate a csv index dynamically for use in rebuilding.')
def index_gen(path:str):
    """Handles index generation requests from the user.
    Args:
        path:   The path to the files in the form of the original file name.
    """
    out=breaker.index_gen(path) # out is a 2 bool list
    if out[0]==True:
        print(f'A new part index file has been generated and has not over written the old one.')
    if out[1]==True:
        print(f'A new tar index file has been generated and has not over written the old one.')

@app.command(help='Segments files into different sections.')
def file_break(path:str,
               size:Annotated[int,typer.Argument()]=default_size,
               csv:Annotated[bool,typer.Option('--csv','-c')]=True):
    """Handles file break requests from the user.
    Args:
        path:   The path to the files in the form of the original file name.
        size:   Size of the resulting chunked files before compression.
        csv:    If a csv index file should be created.
    """
    breaker.file_break(path,size,False,csv,True)

@app.command(help='Rebuilds files that have been broken.')
def file_join(path:str,
              gen:Annotated[bool,typer.Option('--gen','-g')]=True):
    """Handles file join requests from the user.
    Args:
        path:   The path to the files in the form of the original file name.
        gen:    If the csv index file should be generated on the fly.
        """
    # index generation handling
    out=False,False
    if gen==True:
        out=breaker.index_gen(path) # out is a 2 bool list
    if out[0]==True:
        part_override=f'{path}.new'
    else:
        part_override='null' # null is filtered out on the lib side
    if out[1]==True:
        tar_override=f'{path}.new'
    else:
        tar_override='null' # same as above
    # builder
    breaker.file_build(path,part_override,tar_override)

# your a coder harry!
if __name__=='__main__':
    app()
    # Typer is much easier than argparse and at least a little bit easier than Click
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