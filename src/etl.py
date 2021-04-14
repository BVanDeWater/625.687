#! /usr/bin/env python3

"""
Module to pull the dataset into a SQLite database.

"""
import argparse
import h5py as h5
import os
import pandas as pd
import pickle
import glob

EXCLUDE_FIELDS = []
#INCLUDE_FIELDS = []

def build_parser():
    """
    Dropping this at the top for legibility (reading args)
    :return:

    Usage: something like:

        python3 etl.py -t -d /Volumes/T7/MillionSongSubset/ -o ./ -f track_id year artist_latitude artist_longitude

    """
    parser = argparse.ArgumentParser(description='ETL for the MillionSongDataset.')
    parser.add_argument('-d', '--data_path', type=str, dest='data_path', action='store', required=True,
                        help='path to the directory containing your (downloaded) dataset.')
    parser.add_argument('-t', '--test', dest='test', action='store_true', required=False, default=False,
                        help='flag for test (100-long dataframe).')
    parser.add_argument('-f', '--fields', nargs='+', required=False, action='store', dest='fields',
                        help='list of fields to include.')
    parser.add_argument('-o', '--output', type=str, dest='output_path', action='store', required=False, default="",
                        help='path to output file. Defaults to basedir.')
    return parser


########
# MAIN #
########

def main(basedir, output_path, test):
    # Initialize a list to collect file features.
    data_list = list()

    # Walk through the hierarchy to gather paths for each h5 file.
    br = False
    cnt = 0
    print()
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + '.h5'))
        for f in files:
            print(f"\r\033[A{cnt}     {INCLUDE_FIELDS}")
            try:
                data_list.append(pull_attrs_from_h5(f))
                cnt += 1
            except:
                print(f"Error at {cnt}\n")
                continue
            if test and cnt >= 100:
                br = True
                break
        if br:
            break


    agg_df = pd.DataFrame(data_list)

    if test:
        test_st = '_test'
    else:
        test_st = ''

    if INCLUDE_FIELDS:
        field_st = '.' + '_'.join(INCLUDE_FIELDS)
    else:
        field_st = ''

    path = f'{output_path}MillionSongSubset_dataframe{test_st}{field_st}.pkl'
    with open(path, 'wb') as f:
        pickle.dump(agg_df, f)
    print(path)


#############
# FUNCTIONS #
#############

def apply_to_all_files(basedir, func=lambda x: x, ext='.h5'):
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
        files = glob.glob(os.path.join(root, '*' + ext))
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
        if type(f_h5[i]) == h5._hl.dataset.Dataset:
            file_attrs = process_ds(f_h5[i], file_attrs)
    return file_attrs


def process_group(grp, attrs):
    for k in grp.keys():
        if type(grp[k]) == h5._hl.group.Group:
            attrs = process_group(grp[k], attrs)
        elif type(grp[k]) == h5._hl.dataset.Dataset:
            attrs = process_ds(grp[k], attrs)
    return attrs


def process_ds(ds, attrs):
    if ds.dtype.names:
        for field in ds.dtype.names:
            if INCLUDE_FIELDS \
                and field in INCLUDE_FIELDS \
                and field not in EXCLUDE_FIELDS:
                attrs[field] = ds[field][0]
            elif EXCLUDE_FIELDS \
                and field not in EXCLUDE_FIELDS:
                attrs[field] = ds[field][0]
    elif type(list(ds[()])) == h5._hl.dataset.Dataset:
        attrs = process_ds(list(ds[()]), attrs)
    else:
        vals = []
        if INCLUDE_FIELDS \
            and ds.name.split("/")[-1] in INCLUDE_FIELDS \
            and ds.name.split("/")[-1] not in EXCLUDE_FIELDS:
            for ele in ds:
                vals.append(ele)
            attrs[ds.name.split("/")[-1]] = vals
        elif EXCLUDE_FIELDS \
            and ds.name.split("/")[-1] not in EXCLUDE_FIELDS:
            for ele in ds:
                vals.append(ele)
            attrs[ds.name.split("/")[-1]] = vals
    return attrs


#######
# RUN #
#######

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    data_path = args.data_path
    test = args.test

    if args.fields:
        global INCLUDE_FIELDS
        INCLUDE_FIELDS = args.fields

    if args.output_path:
        output_path = args.output_path
    else:
        output_path = data_path

    main(data_path, output_path, test)
