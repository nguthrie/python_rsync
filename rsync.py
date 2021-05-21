#!/usr/bin/python3

import os
import sys
import getopt
import shutil
import filecmp

HELP = '''Python rsync  version 0.1  protocol version 1
Copyright (C) 2021 by Nicholas Guthrie.
GitHub: https://github.com/nguthrie/python_rsync.git

Python rsync is a mininmal analog of rsync written in Python. Python rsync is a file transfer program.
It transfers files in a filetree that is one level deep. It will only transfer files if they have different 
contents.

Usage: rsync [OPTION]... SRC ... DEST

Example:  
- python rsync file dir/ will copy file into dir/
- python rsync -d(--dirs) dir1/ dir2/ will copy contents of dir1/ into dir2/

Options: 
-d, --dirs                  transfer directories without recursing
-n, --dry-run               perform a trial run with no changes made and prints transfer list
-h, --help                  show this help (-h is --help only if used alone)
v, --verbose                increase verbosity'''


def main(argv=None):
    """
    Python rsync is a mininmal analog of rsync written in Python. Python rsync is a file transfer program.
    It transfers files in a filetree that is one level deep. It will only transfer files if they have
    different contents.

    :param argv: list of strings (usually taken from CLI, but optionally passed directly for testing)
    :return:
    """

    # allow passing of arguments to test
    if not argv:
        argv = sys.argv[1:]

    def parse_input(argv):
        """
        Parses CLI input into options and arguments

        :param argv: list of strings
        :return: list of strings, list of strings
        """

        unix_options = "nhdv"
        gnu_options = ["dry-run", "help", "dirs", "verbose"]

        try:
            opts, args = getopt.getopt(argv, unix_options, gnu_options)

        except getopt.GetoptError as error:
            print(error)
            sys.exit(1)

        return opts, args

    def get_transfer_candidates(args):
        """
        Checks existence of inputs against files and directories in source folder.

        :param args: list of strings
        :return: list of strings
        """

        transfer_candidates = []

        for item in args[:-1]:
            abs_path_to_source = os.path.join(os.getcwd(), item)
            source_is_dir = os.path.isdir(abs_path_to_source)
            source_is_file = os.path.isfile(abs_path_to_source)
            if source_is_file:
                transfer_candidates.append(abs_path_to_source)
            elif source_is_dir and dirs:
                transfer_candidates.append(abs_path_to_source)
            elif source_is_dir and not dirs:
                report.append('skipping directory {}'.format(os.path.basename(os.path.normpath(abs_path_to_source))))

        return transfer_candidates

    def sync(transfer_candidates):
        """
        Copies candidates to target folder if they do not exist or hashes are different.
        Note: Like bash rsync, allows mapping many files to one - will create the file if it doesn't exist.

        :param transfer_candidates: list of strings
        :return: None
        """

        abs_path_to_dest = os.path.join(os.getcwd(), arguments[-1])
        dest_is_dir = os.path.isdir(abs_path_to_dest)

        for candidate in transfer_candidates:
            if os.path.isfile(candidate):
                candidate_basename = os.path.basename(candidate)
            else:
                candidate_basename = os.path.basename(os.path.normpath(candidate))
            candidate_dirname = os.path.dirname(abs_path_to_dest)
            path_to_candidate_in_dest = os.path.join(candidate_dirname, candidate_basename)
            if os.path.exists(path_to_candidate_in_dest) and dest_is_dir:
                if os.path.isfile(candidate):
                    hashes_match = filecmp.cmp(candidate, path_to_candidate_in_dest)
                    if not hashes_match:
                        report.append(candidate_basename)
                        if not dry_run:
                            shutil.copy(candidate, path_to_candidate_in_dest)
            elif os.path.isfile(candidate):
                if os.path.exists(abs_path_to_dest):
                    hashes_match = filecmp.cmp(candidate, abs_path_to_dest)
                    if not hashes_match:
                        report.append(candidate_basename)
                        if not dry_run:
                            shutil.copy(candidate, path_to_candidate_in_dest)
                else:
                    report.append(candidate_basename)
                    if not dry_run:
                        shutil.copy(candidate, abs_path_to_dest)
            else:
                if os.path.isfile(candidate):
                    report.append(candidate_basename)
                    if not dry_run:
                        shutil.copy(candidate, path_to_candidate_in_dest)
                else:
                    if os.path.splitext(abs_path_to_dest)[1]:
                        continue
                    report.append(os.path.basename(os.path.normpath(candidate)))
                    if not dry_run:
                        shutil.copytree(candidate, path_to_candidate_in_dest)

    def print_report(report):
        """
        Formats and prints files and directories that will be transferred (if not dry-run).

        :param report: list of strings
        :return: None
        """

        [print(line) for line in report]
        print()
        print("sent ??? bytes  received ??? bytes  ??? bytes/sec")
        if dry_run:
            print("total size is ???  speedup is ??? (DRY RUN)")
        else:
            print("total size is ???  speedup is ???")

    options, arguments = parse_input(argv)

    dirs = False
    dry_run = False
    verbose = False

    report = []

    for opt, arg in options:
        if opt == '-h' or opt == '--help':
            print(HELP)
            sys.exit()

        if opt == '-d' or opt == '--dirs':
            dirs = True

        if opt == '-n' or opt == '--dry-run':
            dry_run = True

        if opt == '-v' or opt == '--verbose':
            verbose = True

    candidates = get_transfer_candidates(arguments)

    sync(candidates)

    if dry_run or verbose:
        print_report(report)


if __name__ == "__main__":
    main()
