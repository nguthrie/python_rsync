import shutil
import os
import sys

# src, dest = sys.argv[1:]


wd = os.getcwd()

new_file_path = os.path.join(wd, "tests")
for i in range(5):
    f = open(os.path.join(wd, "tests/source/file{}.txt".format(i)), "w")


print(wd)



src = os.path.join(wd, "tests/source/file1.txt")

print("source:", src)

dest = os.path.join(wd, "tests/dest/")

print("dest:", dest)

# can be filename or directory for output location
shutil.copy(src, dest)

# NOT DOING - ONLY ONE LEVEL DEEP!
# useful for recusive with regex
# for folders, subfolders, filenames in os.walk(source_folder):
    # for filename in filenames:
    #     if filename.endswith(‘{}’.format(extension)):
    #         shutil.copy(os.path.join(folders, filename), destination_folder)