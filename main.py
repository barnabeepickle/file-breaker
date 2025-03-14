"""CLI tool for splitting files, compressing them and reassembling them"""
# imports
import os
import argparse
import tarfile

# func
def file_split_bysize(input_file,chunk_size):
    """Splits a file into smaller chunks by size.
    Args:
        input_file: Path to the input file.
        chunk_size: Maximum size of each chunk in bytes.
    """
    if not os.path.getsize(input_file)<=chunk_size or os.path.getsize(input_file)==chunk_size: 
        file_number=1
        with open(input_file,'rb') as file:
            while True:
                chunk=file.read(chunk_size)
                if not chunk:
                    break
                output_file=f'{input_file}.part_{file_number}'
                with open(output_file,'wb') as outfile:
                    outfile.write(chunk)
                file_number+=1
    else:
        print('File is smaller than or equal to chunk size, not splitting file')

# Example usage:
file_path='README.md' # input file path
chunk_size_bytes=1024*1024 # 1MB
file_split_bysize(file_path,chunk_size_bytes)