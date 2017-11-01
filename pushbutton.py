#!/usr/bin/env python
"""
Pushbutton is a shiny facade for any polyglot mess
"""
from __future__ import print_function
import os
import sys
import subprocess

# magic files
_F_ALL = ".all"
_F_EXEC = ".exec"
_F_HELP = ".help"
_F_list = ".list"

# magic args
_A_ALL = "all"
_A_HELP = "help"
_A_LIST = "list"


def _exec(fpath, args):
    return subprocess.call([fpath] + args)


def _get_options(path):
    return [i for i in os.listdir(path) if not i.startswith(".")]


def _list_dir(path, args):
    print("Hi! Your options are: %s" % _get_options(path))


def _help_for_dir(path, args):
    # magic .help overrides default help
    if os.path.isfile(os.path.join(path, _F_HELP)):
        _exec(os.path.join(path, _F_HELP), args)
    _default_help(path, args)


def _default_help(path, args):
    print("you ran %s with args %s" % (path, args))
    print("valid options are: %s" % _get_options(path))


def pushbutton_exec_file(path, args):
    return _exec(path, args)


def pushbutton_exec_dir(path, args):
    # magic .exec overrides default behavior
    if os.path.isfile(os.path.join(path, _F_EXEC)):
        return _exec(os.path.join(path, _F_EXEC), args)

    if args:
        # magic args for *all* and *help*
        if args[0] == _A_ALL:
            print("TODO run all")
            # TODO error code when running multiple things
            return 0
        elif args[0] == _A_HELP:
            _help_for_dir(path, args[1:])
            return 0
        elif args[0] == _A_LIST:
            _list_dir(path, args[1:])
            return 0

    _help_for_dir(path, args)
    return 1


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
    sys.exit(pushbutton_navigate(tree, args))


if __name__ == "__main__":
    _main()
