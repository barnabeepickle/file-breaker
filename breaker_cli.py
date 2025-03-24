"""The CLI interface for file_breaker using typer."""
# imports
import file_breaker as breaker
import typer
from typing_extensions import Annotated

# some vars
default_size=1024*1024*50
app=typer.Typer()

# func
@app.command()
def index_gen(path:str): # handles index generation
    out=breaker.index_gen(path)
    if out[0]==True:
        print(f'A new part index file has been generated and has not over written the old one.')
    if out[1]==True:
        print(f'A new tar index file has been generated and has not over written the old one.')

@app.command()
def file_break(path:str,
               size:Annotated[int,typer.Argument()]=default_size,
               csv:Annotated[bool,typer.Argument()]=True):
    breaker.file_break(path,size,False,csv,True)

@app.command()
def file_join(path:str,
              size:Annotated[int,typer.Argument()]=default_size,
              gen:Annotated[bool,typer.Argument()]=False):
    # index generation handling
    out=False,False
    if gen==True:
        out=breaker.index_gen(path)
    if out[0]==True:
        part_override=f'{path}.new'
    else:
        part_override='null'
    if out[1]==True:
        tar_override=f'{path}.new'
    else:
        tar_override='null'
    # builder
    breaker.file_build(path,part_override,tar_override)

# your a coder harry!
if __name__=='__main__':
    app()
    # Typer is much easier than argparse and at least a little bit easier than Click