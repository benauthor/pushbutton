#!/usr/bin/env python
"""
Pushbutton is a shiny facade for any polyglot mess
"""
from __future__ import print_function
import os
import sys

# magic files
_F_ALL = ".all"
_F_EXEC = ".exec"
_F_HELP = ".help"
_F_list = ".list"

# magic args
_A_ALL = "all"
_A_HELP = "help"
_A_LIST = "list"


def pushbutton_exec_file(path, args):
    print('exec this file')
    print(path)
    print(args)


def pushbutton_exec_dir(path, args):
    print('exec this dir')
    print(path)
    print(args)
    # default: do custom .exec
    # default: do custom .help
    # default: do deafult .help which is list commands


def pushbutton_exec(path, args):
    if os.path.isdir(path):
        return pushbutton_exec_dir(path, args)
    return pushbutton_exec_file(path, args)


def pushbutton_navigate(tree, args):
    if not args:
        return pushbutton_exec(tree, [])

    walker = os.walk(tree)
    nextcmd, nextargs = args[0], args[1:]

    root, dirs, files = next(walker)

    if nextcmd in dirs and nextcmd in files:
        raise RuntimeError(
            "Ambiguous command, %s is both a dir and a file" % nextcmd)

    nextpath = os.path.join(root, nextcmd)

    if nextcmd in files:
        return pushbutton_exec(nextpath, nextargs)
    elif nextcmd in dirs:
        return pushbutton_navigate(nextpath, nextargs)
    else:
        return pushbutton_exec(tree, args)


def _main():
    tree = sys.argv[1]
    args = sys.argv[2:]
    pushbutton_navigate(tree, args)


if __name__ == "__main__":
    _main()
