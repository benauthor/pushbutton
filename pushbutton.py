#!/usr/bin/env python
"""
Pushbutton is a shiny facade for any polyglot mess
"""
from __future__ import print_function
import os
import sys
import subprocess

_BASENAME_ENV = "PUSHBUTTON_BASENAME"
_BASENAME = os.environ.get(_BASENAME_ENV, "pushbutton")

# magic files
_F_ALL = ".all"
_F_EXEC = ".exec"
_F_HELP = ".help"
_F_LIST = ".list"

# magic args
_A_ALL = "all"
_A_HELP = "help"
_A_LIST = "list"

_MAGIC_ARGS = (_A_ALL, _A_HELP, _A_LIST)


def _exec(fpath, args):
    return subprocess.call([fpath] + args)


def _get_options(path):
    return [i for i in os.listdir(path) if not i.startswith(".")]


def _list_action(path, args):
    print("subcommands: %s" % ", ".join(_get_options(path)))
    return 0


def _help_action(path, args, stack):
    """
    N.B. caller determines exit code!
    """
    # magic .help overrides default help
    if os.path.isfile(os.path.join(path, _F_HELP)):
        _exec(os.path.join(path, _F_HELP), args)
    _default_help(path, args, stack)


def _default_help(path, args, stack):
    """
    N.B. caller determines exit code!
    """
    print("Usage: %s SUBCOMMAND" % " ".join(stack))
    _list_action(path, args)
    print("(you could also say: %s)" % ", ".join(_MAGIC_ARGS))
    if args:
        print("You said: %s" % " ".join(args))


def _all_action(path, args):
    # magic .all overrides default help
    if os.path.isfile(os.path.join(path, _F_ALL)):
        return _exec(os.path.join(path, _F_ALL), args)
    return _default_all(path, args)


def _default_all(path, args):
    code = 0
    for action in _get_options(path):
        code += _exec(os.path.join(path, action), args)
    return code


def pushbutton_exec_file(path, args):
    return _exec(path, args)


def pushbutton_exec_dir(path, args, stack):
    if args:
        if args[0] == _A_ALL:
            return _all_action(path, args)
        elif args[0] == _A_HELP:
            _help_action(path, args[1:], stack)
            return 0
        elif args[0] == _A_LIST:
            return _list_action(path, args[1:])

    # magic .exec overrides default behavior
    if os.path.isfile(os.path.join(path, _F_EXEC)):
        return _exec(os.path.join(path, _F_EXEC), args)

    _help_action(path, args, stack)
    return 1


def pushbutton_exec(path, args, stack):
    if os.path.isdir(path):
        return pushbutton_exec_dir(path, args, stack)
    return pushbutton_exec_file(path, args)


def pushbutton_navigate(tree, args, stack=(_BASENAME,)):
    if not args:
        return pushbutton_exec(tree, [], stack)

    walker = os.walk(tree)
    nextcmd, nextargs = args[0], args[1:]

    root, dirs, files = next(walker)
    nextpath = os.path.join(root, nextcmd)

    if nextcmd in files:
        return pushbutton_exec(nextpath, nextargs, stack)
    elif nextcmd in dirs:
        return pushbutton_navigate(
            nextpath, nextargs, stack=stack + (nextcmd,),
        )
    else:
        return pushbutton_exec(tree, args, stack)


def _main():
    tree = sys.argv[1]
    args = sys.argv[2:]
    sys.exit(pushbutton_navigate(tree, args))


if __name__ == "__main__":
    _main()
