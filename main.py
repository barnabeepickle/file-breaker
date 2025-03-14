"""CLI tool for splitting files, compressing them and reassembling them"""
# imports
import os
import argparse
import tarfile
import csv

# func
def file_split(input_file,chunk_size,compress=True,build_csv=True,remove_part=True):
    """Splits a file into smaller chunks by size.
    Args:
        input_file: Path to the input file.
        chunk_size:     Maximum size of each chunk in bytes.
        compress:       Bool, if part files should be compressed.
        build_csv:      Bool, if .csv files should be created for putting parts back together.
        remove_part:    Bool, if divided part files should be removed once compressed
    """
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
                    part_index.writerow([output_file])
                if compress==True: # this section of code handles compressing the part files
                    try: # use try to check if a tar file is there, will try to open it if so
                        tar=tarfile.open(f'{output_file}.tar','x:xz')
                    except: # might change this later to have through an error or something like that
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

def list_to_str(item):
    item=str(item)
    item=item.strip('\'",[]')
    return item

def file_join(og_filename):
    """Joins split files back together.
    Args:
        og_filename:    The file name of the original file, used to make all other file names.
    """
    path_part_index=f'{og_filename}.csv'
    if os.path.isfile(path_part_index)==True:
        with open(path_part_index,newline='') as part_index:
            reader=csv.reader(part_index)
            part_index=list(reader)
    path_tar_index=f'{og_filename}.tar.csv'
    if os.path.isfile(path_tar_index)==True:
        with open(path_tar_index,newline='') as tar_index:
            reader=csv.reader(tar_index)
            tar_index=list(reader)
    for x in range(0,len(tar_index)):
        tar_path=list_to_str(tar_index[x])
        part_path=list_to_str(part_index[x])
        with tarfile.open(tar_path) as tar:
            tar.extract(part_path)
    x=0
    del(tar_path)
    with open(f'new.{og_filename}','ab') as final_file:
        for x in range(0,len(part_index)):
            part_path=list_to_str(part_index[x])
            with open(part_path,'rb') as current_file:
                final_file.write(current_file)
            os.remove(part_index[x])
    del(x,part_path)

# Example usage:
file_path='django_logo.png' # input file path
# chunk_size=1024*1024*50 # 50MB i think
chunk_size=100000 # testing file size
file_split(file_path,chunk_size)
file_join(file_path)