#! /usr/bin/env python3

"""
Module to pull the dataset into a SQLite database.

"""
import os, sys
import glob
import h5py as h5
import sqlite3 as sql

import numpy as np
import pandas as pd
from tqdm import tqdm

IGNORE_FIELDS = ['track7_digitalid', '']

########
# MAIN #
########

def main(basedir, test):
    # Initialize a list to collect file features.
    data_list = list()

    # Walk through the hierarchy to gather paths for each h5 file.
    br = False
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+'.h5'))
        for f in files:
            #try:
            print(cnt)
            try:
                data_list.append(pull_attrs_from_h5(f))
                cnt += 1
            except:
                continue
            if test and cnt > 100:
                br = True
                break
        if br:
            break

    agg_df = pd.DataFrame(data_list)
    print(agg_df)

    # Pickle the DataFrame?
    agg_df.to_pickle(f'{basedir}/MillionSongSubset_dataframe.zip')


#############
# FUNCTIONS #
#############

def apply_to_all_files(basedir,func=lambda x: x,ext='.h5'):
    """
    ** Adapted from the MSD Python Tutorial **

    From a base directory, go through all subdirectories,
    find all files with the given extension, apply the
    given function 'func' to all of them.
    If no 'func' is passed, we do nothing except counting.
    INPUT
       basedir  - base directory of the dataset
       func     - function to apply to all filenames
       ext      - extension, .h5 by default
    RETURN
       number of files
    """
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files:
            func(f)   
    return cnt

def pull_attrs_from_h5(f):
    file_attrs = {}
    f_h5 = h5.File(f, 'r')
    for i in f_h5.keys():
        if type(f_h5[i]) == h5._hl.group.Group:
            file_attrs = process_group(f_h5[i], file_attrs)
    return file_attrs


def process_group(grp, attrs):
    for k in grp.keys():
        if type(grp[k]) == h5._hl.group.Group:
            process_grp(grp[k], attrs)
        elif type(grp[k]) == h5._hl.dataset.Dataset:
            process_ds(grp[k], attrs)
    return attrs

def process_ds(ds, attrs):
    if ds.dtype.names:
        for field in ds.dtype.names:
            if field in IGNORE_FIELDS:
                continue
            attrs[field] = ds[field][0]
    return attrs

#######
# RUN #
#######

if __name__ == '__main__':
    # Hacky argparsing, lol.
    test = False
    for token in ["-t", "--test", "t", "test"]:
        if token in sys.argv:
            test=True
    if 'ben' in sys.argv or 'Ben' in sys.argv:
        basedir = "/Volumes/T7/MillionSongSubset"
    else:
        basedir = "" # Your path here!

    main(basedir, test)