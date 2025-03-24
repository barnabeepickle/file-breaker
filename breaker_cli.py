"""The CLI interface for file-breaker."""
# imports
import file_breaker as breaker
import argparse
import pathlib

# vars
default_size=1024*1024*50
mode_key={'break':0,'rebuild':1,'gen':2}

# argparse has been sent to the shadow realm

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