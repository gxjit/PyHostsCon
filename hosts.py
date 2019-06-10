

# Copyright (c) 2019 Gurjit Singh

# This source code is licensed under the MIT license that can be found in
# the accompanying LICENSE file or at https://opensource.org/licenses/MIT.


import argparse
import pathlib
import sys

def parseArgs():

    def dirPath(pth):
        pthObj = pathlib.Path(pth)
        if pthObj.is_dir():
            return pthObj
        else:
            raise argparse.ArgumentTypeError("Invalid Directory path")

    parser = argparse.ArgumentParser(description="Filter and concatenate \
                                     HOSTS entries from *.txt files in\
                                     specified folder.")
    parser.add_argument("dir", metavar="DirPath",
                        help="Directory path", type=dirPath)
    pargs = parser.parse_args()

    return pargs


def main(pargs):
    
    dirpath = pargs.dir.resolve()

    filelist = [x for x in dirpath.iterdir()
               if x.is_file() and x.suffix == ".txt"]

    if not filelist:
        print("Nothing to do.")
        sys.exit()

    hostsSet = set()
    for file in filelist:
        with open(file, "r") as openFile:
            for line in openFile:
                if line.startswith("0.0.0.0 "):
                    hostsSet.add(line.strip())

    hostsString = "\n0.0.0.0 0.0.0.0\n"
    hostsString += "\n".join(str(x) for x in hostsSet)
    hostsString += "\n"
    with open(dirpath.joinpath("hosts.tmp"), "w") as hostsTmp:
        hostsTmp.write(hostsString)

main(parseArgs())

# 127.0.0.1 localhost\n
