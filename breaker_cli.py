"""The CLI interface for file-breaker."""
# imports
import file_breaker as breaker
import argparse
import pathlib

# vars
default_size=1024*1024*50

# argparse setup
mode_key={'break':0,'rebuild':1,'igen':2}
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
                    choices=['break','rebuild','igen'],
                    help='If the input file should be broken or reassembled',
                    default='break')
parser.add_argument('-s', '--size',
                    type=int,
                    help='Specify the size in bytes of the output file.',
                    default=default_size)
parser.add_argument('-c','--csv',
                    help='Disable the need for a CSV file (generates index on demand).',
                    action='store_true')
# parse the arguments
path=parser.parse_args(args=['input_path'])
mode=parser.parse_args(args=['mode']) # this doesn't work for some damn reason
mode=mode_key[mode]
size=parser.parse_args(args=['-s','--size'])
# CSV has two uses but it is not fully implemented yet TODO: finish that
csv=parser.parse_args(args=['-c','--csv'])
# i don't know how to write good argparse .parse_args() code, like i really have no clue

# code
if mode==1 and csv==True:
    gen_index=True
if mode==2:
    gen_index=True
if gen_index==True: # handles the -c, --csv, gen_index or mode==2 args
    overrides=breaker.index_gen(path)
    if overrides[0]==True:
        part_override=f'{path}.new'
        if mode==2:
            print(f'The new part index file has been generated with the name: {part_override}')
    else: # setting your override to 'null' causes it to be filtered out
        part_override='null'
    if overrides[1]==True:
        tar_override=f'{path}.new'
        if mode==2:
            print(f'The new tar index file has been generated with the name: {tar_override}')
    else: # same as the other 'null' filter override
        tar_override='null'
    if mode==2:
        print('The new index files have been generated correctly.') # got that feedback to the user
if mode==0:
    breaker.file_break(path,size,build_csv=not csv) # is this valid code?
elif mode==1:
    breaker.file_build(path,part_override,tar_override) # it always uses the override values 
    # but uses the 'null' filter to make simpler code happen, uses this at your own risk