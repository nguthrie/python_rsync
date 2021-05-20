#!/usr/bin/python3

import os
import sys
import getopt
import shutil
import filecmp


with open("help.txt") as f:
   HELP = f.read()


def main():

    argv = sys.argv[1:]

    def parse_input(argv):

        unixOptions = "nhdv"
        gnuOptions = ["dry-run", "help", "dirs", "verbose"]

        try:
            opts, args = getopt.getopt(argv, unixOptions, gnuOptions)
            print("(test output) opts:", opts)
            print("(test output) args:", args)

        # can enter any number of args
        # also can handle unix globs!!!
        
        # will get all files that match from the directory if they exists

        except getopt.GetoptError as error:
            print(error)
            sys.exit(1)
    
        return opts, args



    opts, args = parse_input(argv)

    # get source directory
    # select files to transfer or print
    print()
    print("number of matching source args", len(args[:-1]))

    dirs = False
    dry_run = False
    verbose = False

    # TO DO: do a faster, better looking checking
    # functionality: just check for -h/--help
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(HELP)
            sys.exit()
        
        if opt == '-d' or opt == '--dirs':
            dirs = True

        if opt == '-n' or opt == '--dry-run':
            dry_run = True
        
        if opt == '-v' or opt == '--verbose':
            verbose = True

    transfer_candidates = []
    report = []

    for item in args[:-1]:
        # input files may or may not match input files
        abs_path_to_source = os.path.join(os.getcwd(), item)
        basename =  os.path.basename(abs_path_to_source)
        print("source basename:", basename)
        dirname = os.path.dirname(abs_path_to_source)
        print("source dirname:", dirname)
        path_split = os.path.split(abs_path_to_source)
        print("source split:", path_split)
        extension = os.path.splitext(abs_path_to_source)[1]
        print("source extension:", extension)
        source_exists = os.path.exists(abs_path_to_source)
        print("does source exists? ", source_exists)
        source_is_dir = os.path.isdir(abs_path_to_source)
        print("is source a dir? ", source_is_dir)
        source_is_file = os.path.isfile(abs_path_to_source)
        print("is source a file? ", source_is_file)
        # * will never be in the extension
        # print("* in extension?", "*" in extension)
        print("* in basename?", "*" in basename)
        print()
        # all I'm doing is checking if the path is a file or a dir
        # if it is (and dirs), and it to the transfer candidates list
        if source_is_file:
            transfer_candidates.append(abs_path_to_source)
        elif source_is_dir and dirs:
            transfer_candidates.append(abs_path_to_source)
        elif source_is_dir and not dirs:
            report.append('skipping directory {}'.format(os.path.basename(os.path.normpath(abs_path_to_source))))

    print("transfer candidates:", transfer_candidates)
    print()



    abs_path_to_dest = os.path.join(os.getcwd(), args[-1])
    print("abs path to dest:", abs_path_to_dest)
    dest_is_dir = os.path.isdir(abs_path_to_dest)
    print('dest is dir:', dest_is_dir)
    dest_is_file = os.path.isfile(abs_path_to_source)
    print('dest is file:', dest_is_file)


    for candidate in transfer_candidates:
        print('candidate:', candidate)
        if os.path.isfile(candidate):
            candidate_basename = os.path.basename(candidate)
        else:
            candidate_basename = os.path.basename(os.path.normpath(candidate))
        print('candidate basename:', candidate_basename)
        candidate_dirname = os.path.dirname(abs_path_to_dest)
        print("candidate dirname:", candidate_dirname)
        path_to_candidate_in_dest = os.path.join(candidate_dirname, candidate_basename) 
        print('candidate in dest:', path_to_candidate_in_dest)
        # we know the candidate exists
        # check if the candidate exists in the destination folder
        # and the destination is a folder
        if os.path.exists(path_to_candidate_in_dest) and dest_is_dir:
            print("file/dir exists and dest is dir")
            # hash compare files to see if transfer is needed
            # if files are not the same
            # if directory exists, that's sufficient, don't need to check 
            if os.path.isfile(candidate):
                hashes_match = filecmp.cmp(candidate, path_to_candidate_in_dest)
                print("dest is folder and hashes match:", hashes_match)            
                if hashes_match != True:
                    report.append(candidate_basename)
                    if dry_run != True:
                        shutil.copy(candidate, path_to_candidate_in_dest)
            # elif os.path.isdir(candidate) and dirs:
            #     # DO NEED THIS BECAUSE DIR EXISTS IN DEST
            #     # HASH WILL SAY DIFF BUT CAN'T BE DIFF BC EMPTY (ONE LEVEL)
            #     # NOTHING TO DO OR REPORT
            #     # if the directory exists, we don't need to copy
            #     # the directory can't have any contents
            #     # just add to the report
            #     report.append(os.path.basename(os.path.normpath(candidate)))
        elif dest_is_file:
            if os.path.exists(abs_path_to_dest):
                hashes_match = filecmp.cmp(candidate, abs_path_to_dest) 
                print("dest is file and hashes match:", hashes_match)
                if hashes_match != True:
                    report.append(candidate_basename)
                    if not dry_run:
                        shutil.copy(candidate, path_to_candidate_in_dest)
            else:
                report.append(candidate_basename)
                if not dry_run:
                    shutil.copy(candidate, abs_path_to_dest)
        else:
            print("file/dir does not exist in destination")
            if os.path.isfile(candidate):
                report.append(candidate_basename)
                if not dry_run:
                    shutil.copy(candidate, path_to_candidate_in_dest)
            else:
                # is directory that doesn't exist in the dest folder
                report.append(os.path.basename(os.path.normpath(candidate)))
                if not dry_run:
                    shutil.copytree(candidate, path_to_candidate_in_dest)

    def print_report(report):
        
        [print(line) for line in report]
        print()
        print("sent ??? bytes  received ??? bytes  ??? bytes/sec")
        if dry_run:
            print("total size is ???  speedup is ???" + " (DRY RUN)")
        else:
            print("total size is ???  speedup is ???")

    if dry_run or verbose:
        print_report(report)



if __name__ == "__main__":
    
    main()