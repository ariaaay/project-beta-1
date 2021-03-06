
""" Functions to save create consistent names and folders in scripts. 
    This will also save an array of objects into seperate files in one folder.  
    ADD MORE
""" 

import numpy as np
import matplotlib.pyplot as plt
import os

BASE_PATH = os.getcwd()

def make_filname(root, index, ext):
    name =  root + '_' + str(index) + '.' + ext
    return name

def make_folder(typ, fold_name):
    assert os.getcwd() == BASE_PATH #Make sure in right directory
    if not os.path.exists(typ):
        os.makedirs(typ) 
    os.getcwd()
    os.chdir(typ)
    if not os.path.exists(fold_name):
        os.mkdir(fold_name)
    os.chdir('..') #Return back to working directory  
    return fold_name

def save_object(obj, foldername, typ, filename, is_plt):
    assert os.getcwd() == BASE_PATH #Make sure in right directory
    os.chdir(typ) 
    os.chdir(foldername)
    if is_plt:
        plt.savefig(filename)
    else:
        np.save(filename, obj) #FIX adds .npz extension 
    os.chdir('..')
    os.chdir('..') 
    path = './' + typ + '/' + foldername + '/' + filename
    return path 

def save_all(arr, fileroot, typ, folder_root, ext):
    """ 
    Saves each element in the array 'arr' based on root and the index of
    the element. 'typ' must be either 'txt', data', or 'other'. 
    At this point, this can't save plots (need to use 'save_plt' below).
        
    Example
    -------
    >>> arr = [obj1, obj2, obj3]
    >>> fileroot = 'RMS'
    >>> ext = 'pdf'
    >>> typ = 'data'
    >>> folder_root = RMS
    >>> paths = save_all_plt(arr, fileroot, typ, folder_root, ext)
    >>> print(paths)
    ./data/RMS/RMS_0.pdf
    ./data/RMS/RMS_1.pdf
    ./data/RMS/RMS_2.pdf
    """
    assert typ in ['txt', 'data', 'other']
    paths = []
    foldername = make_folder(typ, folder_root)
    for index, obj in enumerate(arr):
        filename = make_filname(fileroot, index, ext)
        path = save_object(obj, foldername, typ, filename, is_plt=False)
        paths.append(path)
        print('Created ' + filename + ' in ' + './' + typ + '/' + foldername)
    return paths

def save_plt(fileroot, index, folder_root, ext):
    """ADD DES
    """
    foldername = make_folder('figures', folder_root)
    filename = make_filname(fileroot, index, ext)
    save_object('', foldername, 'figures', filename, True)
