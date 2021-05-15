#!/usr/bin/python3

import sys
import os
import sys
import getopt

with open("help.txt") as f:
   HELP = f.read()

def main():
   
    argv = sys.argv[1:]

    # call to handle abs vs relative path...
    # need to handle wether it's
    # a) a directory : os to check if directory
    # b) a file : os to check if is file

    try:
        source = argv[-2]
        destination = argv[-1]
    except IndexError as IE:
        print("Pass at least two arguments")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


    # VALIDATE INPUT FUNCTION

    if os.path.isdir(source):  
        print("\nIt is a directory")  
    elif os.path.isfile(source):  
        print("\nIt is a normal file")  
    else:  
        print("It is a special file (socket, FIFO, device file)" )

    # CHECKS ON prefix with / for absolute path
    IS_ABS = os.path.isabs(source)
    if IS_ABS:
        print("absolute path")
    else:
        print("relavtive path")

    # add call to parse_input() here

    unixOptions = "nhd"
    gnuOptions = ["dry-run", "help", "dirs"]

    try:
        opts, args = getopt.getopt(argv, unixOptions, gnuOptions)
        print("opts:", opts)
        print("args:", args)
    except getopt.GetoptError as error:
        print(error)
        print('test.py -i {} -o {}'.format(source, destination))
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(HELP)
            sys.exit()
        elif opt in ("-n", "--dry-run"):
            pass
        elif opt in ("-d", "--dirs"):
            pass
    
    
    print("Source is {}".format(source))
    print("Destination is {}".format(destination))

def sync():
    pass


if __name__ == "__main__":
    
    main()
    sync()