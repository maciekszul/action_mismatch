import numpy as np
import os

def consecutive_elements(arr, value):
    """
    returns True if array has two consecutive elements (value) in array (arr)
    """
    check = False
    for index, v in enumerate(arr):
        try:
            if (arr[index] == -1) and (arr[index+1] == value):
                check = True
                break
        except IndexError:
            pass
    if arr[0] == -1:
        check = True
    
    return check
    


def tile_shuffle(no_elem, prop_dev):
    """
    no_elem - number of elements in a chunk
    prop_dev - proportion of deviants
    """
    dev_no = int(no_elem * prop_dev)
    reg_no = no_elem - dev_no
    chunk = np.hstack([np.tile(1, reg_no - 1), np.array([0]), np.tile(-1, dev_no)])
    np.random.shuffle(chunk)
    while consecutive_elements(chunk, -1):
        np.random.shuffle(chunk)
    return chunk

def oddball_sequence(no_chunks, no_elem, prop_dev):
    """
    Generates an oddball sequence
    no_chunks - number of chunks 
    no_elem - number of elements in a chunk
    prop_dev - proportion of deviants in each chunk
    """
    return np.tile(tile_shuffle(no_elem, prop_dev), no_chunks)

def mk_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)