#!/usr/bin/env python
# Copyright (c) 2014, Intel Corporation.

import sys, os
from argparse import ArgumentParser
import pandas as pd

def build_argparser():

    usage = '''example:
     python inter_results.py -i '/path/to/root/dir generated by launch.sh i.e. ~/tune/output/default/' 
     -o <optional: path to output dir to save summary_results.csv>
     '''

    parser = ArgumentParser(prog='inter_results.py',
                            description='Intermediate benchmark results',
                            epilog=usage)
    args = parser.add_argument_group('Options')
    args.add_argument('-i', '--input_dir', help='Path to root directory of csv files with model performance data', required=True)
    args.add_argument('-o', '--output_dir', help='Output results summary file .csv', required=False, type=str, default='result_summary.csv')

    return parser

def main():
    
    args = build_argparser().parse_args()

    df_ = pd.DataFrame()

    if not os.path.isdir(args.input_dir):
        print("Error: Invalid root directory")
        return -1
    else:
        root_path = args.input_dir

    l_root_path = len(os.path.normpath(root_path).split(os.path.sep))
    idx = 0
   
    root_instance_dir = []

    for ts, folder in sorted([(os.path.getctime(root_path + dir),root_path + dir) for dir in os.listdir(root_path)]):
        root_instance_dir.append(os.path.normpath(folder).split(os.path.sep)[-1].lower())
    #print("root_instance_dir =", root_instance_dir)

    for curr_dir, list_dirs, file_names in os.walk(root_path):
        l_curr_dir = len(os.path.normpath(curr_dir).split(os.path.sep))
        if l_curr_dir == (l_root_path + 1):
            curr_dir_name = os.path.normpath(curr_dir).split(os.path.sep)[-1]
            idx = root_instance_dir.index(curr_dir_name) + 1
        
        for f in file_names:
            curr_dir_split = os.path.normpath(curr_dir).split(os.path.sep)
            f_ext = os.path.splitext(f)[-1].lower()
            if f_ext == ".csv":
               fn = f.split('-')
               f_csv = os.path.join(curr_dir, f)
               df_csv = pd.read_csv(f_csv)
               df_csv['instance_id'] = [idx]
               df_ = df_.append(df_csv)
    for i, s in enumerate(fn):
        if i == 0:
           st = str('')
        if i > 0 and i < len(fn) - 1:
           st = st + s
        if i >= 1   and i < len(fn) - 2:
           st += '_'
    df_.to_csv(str(st)+".csv", encoding='utf-8', index=False)

if __name__ == '__main__':
    sys.exit(main() or 0)