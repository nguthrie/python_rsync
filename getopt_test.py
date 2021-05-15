#!/usr/bin/python

import sys, getopt

with open("help.txt") as f:
   HELP = f.read()

def main():
   
   argv = sys.argv[1:]

   source = argv[-2]
   destination = argv[-1]

   unixOptions = "rnhi"
   gnuOptions = ["recursive", "dry-run", "help"]

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
      elif opt in ("-i", "--ifile"):
         source = arg
      elif opt in ("-o", "--ofile"):
         destination = arg
   print("Source is {}".format(source))
   print("Destination is {}".format(destination))

if __name__ == "__main__":
   main()