#!/usr/bin/python3

import sys
import os
import sys
import getopt
import glob

with open("help.txt") as f:
   HELP = f.read()

def main():

    argv = sys.argv[1:]

    unixOptions = "nhd"
    gnuOptions = ["dry-run", "help", "dirs"]

    try:
        opts, args = getopt.getopt(argv, unixOptions, gnuOptions)
        print("(test output) opts:", opts)
        print("(test output) args:", args)
        if len(args) != 2:
            print("Please provide a valid source and destination.")
            sys.exit(1)
    except getopt.GetoptError as error:
        print(error)
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(HELP)
            sys.exit()
        
        if opt == '-d' or opt == '--dirs':
            path_handler(True, args)
        else:
            path_handler(False, args)

    # elif opt in ("-n", "--dry-run"):
    #     # determine which files need to be transferred
    #     # print report
    #     # exit
    #     pass
    # elif opt in ("-d", "--dirs"):
    #     pass

def path_handler(dirs, args):
    print("path_handler input:", dirs, args)

    print("dirs", dirs)

    transfer_list = []

    source, dest = args
    cwd = os.getcwd()

    # turn rel path to abs path 
    if not os.path.isabs(source):
        source = os.path.join(cwd, source)
    if not os.path.isabs(dest):
        dest = os.path.join(cwd, dest)

    try:
        print("files in source:", os.listdir(source))
        print("files in dest:", os.listdir(dest))
        source_file = os.listdir(source)
        dest_file = os.listdir(dest)
    except Exception as e:
        print("No such file or directory.")
        exit(1)

    source_is_file = os.path.isfile(source)
    source_is_dir = os.path.isdir(source)
    dest_is_file = os.path.isfile(dest)
    dest_is_dir = os.path.isdir(dest)

    if source_is_file:
        if dest_is_file:
            transfer_list.append((source, dest, 1))
        elif dest_is_dir:
            try:
                shutil.copy(source, dest, 2)
            except Exception as e:
                print(e)
    elif source_is_dir:
        if dest_is_file:
            print('Cannot copy directory to file.')
            exit(1)
        elif dest_is_dir:
            if dirs:
                for objects in os.listdir(source):
                    path_to_object = os.path.join(source, object)
                    transfer_list.append((path_to_object, dest, 3))
            else:
                print("Skipping directory .")
                print("(Add -d/--dir to copy contents.)")
                exit()
    elif source.endswith("*"):
        # use glob to copy over
        for file in glob.glob(source):
            print("debug:", file)
            shutil.copy(file, dest)
    elif "*" in os.path.splittext(source)[1] and not os.path.splittext(source)[1].endswith("*"):
        # wildcard for extensions
        pass  


    if not (source_is_file or source_is_dir):
        print("Cannot handle input.")
        exit(1)


if __name__ == "__main__":
    
    main()