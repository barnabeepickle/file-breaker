"""The CLI interface for file_breaker using typer."""
# imports
import file_breaker as breaker
import typer
from typing_extensions import Annotated

# this code is actually okay, could be better but its works rather well
# (still made in like a half a week with a rewrite part way through)

# some vars
default_size=1024*1024*50
app=typer.Typer() # sets up this as a typer app

# func
@app.command(help='Generate a csv index dynamically for use in rebuilding.')
def index_gen(path:str):
    """Handles index generation requests from the user.
    Args:
        path:   The path to the files in the form of the original file name.
    """
    out=breaker.index_gen(path) # out is a 2 bool list
    # user feedback in the terminal
    if True in out:
        print('A new ',end='')
        if out:
            print('part and tar index files',end='')
        elif False in out:
            if out[0]:
                print('part',end='')
            if out[1]:
                print('tar',end='')
            print(' index file ',end='')
        print('has been generated and has not over written the old one.')

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
    # Potentially add more options to this sub-command
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
    if gen is True:
        out=breaker.index_gen(path) # out is a 2 bool list
    if out[0] is True:
        part_override=f'{path}.new'
    else:
        part_override='null' # null is filtered out on the lib side
    if out[1] is True:
        tar_override=f'{path}.new'
    else:
        tar_override='null' # same as above
    # builder
    breaker.file_build(path,part_override,tar_override)

# your a coder harry! (not a harry potter fan just thought it fit)
if __name__=='__main__':
    app()
    # Typer is much easier than argparse and at least a little bit easier than Click, in my opinion
