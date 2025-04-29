"""A python library for splitting a file into segments and reassembling them."""
# imports
import os
import tarfile
import csv
from convert_str import convert_str

# you probably shouldn't uses this in production (i made this in like a week) 
# and if you still want to use it in production take a look over it
# (submit changes if you have fixes for this mess)

# func
def file_break(input_file,chunk_size,compress=True,build_csv=True,remove_part=True):
    """Splits a file into smaller chunks by size.
    Args:
        input_file: Path to the input file.
        chunk_size:     Maximum size of each chunk in bytes.
        compress:       Bool, if part files should be compressed.
        build_csv:      Bool, if .csv files should be created for putting parts back together.
        remove_part:    Bool, if divided part files should be removed once compressed
    """ # TODO: figure out how to do docstrings better
    if not os.path.getsize(input_file)<=chunk_size or os.path.getsize(input_file)==chunk_size: 
        if build_csv==True: # sets up .csv files (the indexes as labled in the code) that contain file names for rebuilding files
            part_csv=open(f'{input_file}.csv','a',newline='')
            # ripped nearly straight from the csv module documentation
            part_index=csv.writer(part_csv,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
            if compress==True: # sets up the compressed file index
                tar_csv=open(f'{input_file}.tar.csv','a',newline='')
                tar_index=csv.writer(tar_csv,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
        file_number=1 # set/reset the file number for part files
        with open(input_file,'rb') as file:
            while True:
                chunk=file.read(chunk_size)
                if not chunk:
                    break
                output_file=f'{input_file}.part_{file_number}'
                with open(output_file,'wb') as outfile: # creates the new seperated "part" files
                    outfile.write(chunk)
                if build_csv==True: # writes the file name for the part to the part index
                    part_index.writerow([output_file]) # for the file name to be valid it needs to 
                    # be refered to as a list here in the code when writting the value
                if compress==True: # this section of code handles compressing the part files
                    try: # use try to check if a tar file is there, will try to open it if so
                        tar=tarfile.open(f'{output_file}.tar','x:xz')
                    except: # might change this later to have it not go through an error or something like that
                        tar=tarfile.open(f'{output_file}.tar','w:xz') # for now it just tries to open it
                    tar.add(output_file)
                    if remove_part==True:
                        os.remove(output_file)
                    if build_csv==True: # writes the file name for the compressed part to the tar index
                        tar_index.writerow([f'{output_file}.tar'])
                    tar.close()
                file_number+=1
        if build_csv==True: # closes open csv files since this implementation doesn't use the with method
            part_csv.close()
            if compress==True:
                tar_csv.close()
    else:
        print('File is smaller than or equal to chunk size, not splitting file')

def file_build(og_filename,part_csv_override='null',tar_csv_override='null'):
    """Joins split files back together.
    Args:
        og_filename:        The file name of the original file, used to make all other file names.
        part_csv_override:   Overrides the csv filename for the part index, can't be a value of 'null'.
        tar_csv_override:    Overrides the csv filename for the tar index, can't be a value of 'bull'.
    """
    # TODO: add code comments to this function
    if part_csv_override=='null': # can't have the override values default to the filename so this was my solution
        path_part_index=f'{og_filename}.csv'
    else:
        path_part_index=part_csv_override
    if os.path.isfile(path_part_index)==True: # part_index file setup
        with open(path_part_index,newline='') as part_index:
            reader=csv.reader(part_index)
            part_index=list(reader)
    if tar_csv_override=='null': # same as for the other override
        path_tar_index=f'{og_filename}.tar.csv'
    else:
        path_tar_index=tar_csv_override
    if os.path.isfile(path_tar_index)==True: # tar_index file setup
        with open(path_tar_index,newline='') as tar_index:
            reader=csv.reader(tar_index)
            tar_index=list(reader)
    for x in range(0,len(tar_index)):
        tar_path=convert_str(tar_index[x])
        part_path=convert_str(part_index[x])
        with tarfile.open(tar_path) as tar:
            tar.extract(part_path)
    x=0
    del(tar_path)
    with open(f'new.{og_filename}','ab') as final_file:
        for x in range(0,len(part_index)):
            part_path=convert_str(part_index[x])
            with open(part_path,'rb') as current_file:
                final_file.write(current_file.read())
    x=0
    for x in range(0,len(part_index)):
        os.remove(convert_str(part_index[x]))
    del(x,part_path)

def index_gen(file_path):
    """Builds and index automatically.
    Args:
        file_path:  The file name of the original file before being broken, used to make find all other files.
    Returns:
        bool:       Bool to represent if a new part_index file was created.
        bool:       Bool to represent if a new tar_index file was created.
    """
    # index csv file setup
    # part_index csv file setup
    part_new=False
    if os.path.isfile(f'{file_path}.csv')==False:
        part_csv=open(f'{file_path}.csv','a',newline='')
    else:
        part_csv=open(f'{file_path}.new.csv','a',newline='')
        part_new=True
    part_index=csv.writer(part_csv,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    # tar_index csv file setup
    tar_new=False
    if os.path.isfile(f'{file_path}.tar.csv')==False:
        tar_csv=open(f'{file_path}.tar.csv','a',newline='')
    else:
        tar_csv=open(f'{file_path}.tar.new.csv','a',newline='')
        tar_new=True
    tar_index=csv.writer(tar_csv,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    # file finding loop
    x=1
    current_file=f'{file_path}.part_{x}'
    current_tarfile=f'{current_file}.tar'
    while os.path.isfile(current_tarfile)==True:
        print(x)
        part_index.writerow([current_file]) #   same as in file_break these need
        tar_index.writerow([current_tarfile]) # to be weird lists when written
        x+=1
        current_file=f'{file_path}.part_{x}'
        current_tarfile=f'{current_file}.tar'
    del(x)
    return part_new,tar_new

# TODO: Convert these functions into a class, maybe