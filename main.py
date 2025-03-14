"""CLI tool for splitting files, compressing them and reassembling them"""
# imports
import os
import argparse
import tarfile
import csv

# func
def file_split(input_file,chunk_size,compress=True,build_csv=True):
    """Splits a file into smaller chunks by size.
    Args:
        input_file: Path to the input file.
        chunk_size: Maximum size of each chunk in bytes.
        compress:   Bool, if part files should be compressed.
        build_csv: Bool, if .csv files should be created for putting parts back together.
    """
    if not os.path.getsize(input_file)<=chunk_size or os.path.getsize(input_file)==chunk_size: 
        if build_csv==True: # sets up .csv files that contain file names for rebuilding files
            part_csv=open(f'{input_file}.csv','a',newline='')
            part_index=csv.writer(part_csv,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
            if compress==True:
                tar_csv=open(f'{input_file}.tar.csv','a',newline='')
                tar_index=csv.writer(tar_csv,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
        file_number=1
        with open(input_file,'rb') as file:
            while True:
                chunk=file.read(chunk_size)
                if not chunk:
                    break
                output_file=f'{input_file}.part_{file_number}'
                with open(output_file,'wb') as outfile:
                    outfile.write(chunk)
                if build_csv==True:
                    part_index.writerow([output_file])
                if compress==True:
                    try:
                        tar=tarfile.open(f'{output_file}.tar','x:xz')
                    except:
                        tar=tarfile.open(f'{output_file}.tar','w:xz')
                    tar.add(output_file)
                    os.remove(output_file)
                    if build_csv==True:
                        tar_index.writerow([f'{output_file}.tar'])
                    tar.close()
                file_number+=1
        if build_csv==True: # closes open csv files since this implementation doesn't use the with method
            part_csv.close()
            if compress==True:
                tar_csv.close()
    else:
        print('File is smaller than or equal to chunk size, not splitting file')

# Example usage:
file_path='main.py' # input file path
# chunk_size=1024*1024*50 # 50MB i think
chunk_size=1000
file_split(file_path,chunk_size)
