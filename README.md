# Pushbutton

A shiny facade for any polyglot mess

![convenience](https://i.kinja-img.com/gawker-media/image/upload/s--pZMUC9Dt--/c_scale,f_auto,fl_progressive,q_80,w_800/18rvceav6dkkhjpg.jpg)


## What it is

Sometimes you need to write a command line tool. You pick your
favorite scripting language and go to town. Cool!

Now repeat that M times over N years with P collaborators in Q
different scripting languages. Now you have a pile of scripts related
to your system and you forget about some or never heard about that new
one your collaborator wrote.

Pushbutton is basically an organizational strategy for your polyglot
mess that introduces discoverability and a unified entrypoint.

First you make a collection of little executables written in your
preferred scripting language. Organize them into thematically
consistent subdirectories, which will define subcommands:

```
$ cd ~/example
$ ls
cook eat order
$ ./eat
nom nom

$ ls cook
boil braise fry
$ ./cook/boil
bubble!
$ ./cook/fry
sizzle!

$ ls order
pizza random tacos thai
$ ./order/pizza
Who ordered a pizza?
```

Pushbutton gives you a command line interface with some nice magic:

```
$ ./pushbutton.py example help
Subcommands: eat, cook, order
$ ./pushbutton.py example eat
nom nom
$ ./pushbotton.py example cook
You can cook: boil, braise, fry
$ ./pushbutton.py example cook all
bubble!
stew!
sizzle!
```

We can override Pushbutton magic with specially named files.
Let's write an ./order/.exec that hits the `random` subcommand.

```
$ echo '#/bin/bash\
> $(dirname "${BASH_SOURCE[0]}")/random > ./order/.exec
$ ./order/.exec
I see you're feeling indecisive today. Randomly choosing: tacos!
Who ordered tacos?
$ ./pushbutton.py example order
I see you're feeling indecisive today. Randomly choosing: thai!
Who ordered Thai?
```

Ok, cool, but still too much typing! Let's make a shim!

```
$ ./make_pushbutton_shim example foodie
Installed pushbutton shim for ./example/ at /usr/local/bin/foodie
$ foodie cook boil
bubble!
$ foodie order
I see you're feeling indecisive today. Randomly choosing: pizza!
Who ordered pizza?
```

## Installation

The pushbutton script is a free-wheeling, no-install-necessary
rambler. If you've got a relatively modern version of Python installed,
it should Just Work. However the idea is to turn your tree of little
scripts into one glorious command line tool. To do that, run:

     ./make_pushbutton_shim path/to/my/scripts somename

If you move your scripts, everything will break. Oh no! What to do?
Just make a new shim.

## Magics

Magic args are:
- `help`: print the help for the command represented by the directory
- `list`: print all available subcommands in the directory
- `all`: run all the subcommands in the directory

Magic files that override magic behaviors are:
- `.exec`: what to do when running the directory without a
  subcommand. default: print help
- `.all`: custom `all` for the directory. you may want to leave something
  out for some reason.
- `.help`: custom `help` for the directory.
- `.list`: custom `list` for the directory.

## Writing subcommands

Make an executable file in your preferred manner. All excess arguments
will be passed on to your executable in a straightforward manner.
i.e. `foodie cook boil broccoli --minutes 10` is
equivalent to running `./example/cook/boil broccoli --minutes 10`.


## Credit

Credit where credit is due: former coworker
[kmb](https://github.com/kevinbirch) came up with this general
tree-of-lil'-scripts-that-defines-command-line-interface pattern for
some great internal tooling we had at [Percolate](https://github.com/percolate).

I should mention I love [docopt](http://docopt.org/) and use it
whenever I can.  Credit also probably to kmb for heckling me into
loving docopt, now that I think of it.
