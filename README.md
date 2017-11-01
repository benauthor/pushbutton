# Pushbutton

A shiny facade for any polyglot mess

## What it is

Sometimes you need to write a command line tool. You pick your
favorite scripting language and go to town. Cool!

Now repeat that M times over N years with P collaborators in Q
different scripting languages. Now you have a pile of scripts related
to your system and you forget about some or never heard about that new
one your collaborator wrote.

Pushbutton is basically an organizational strategy for your polyglot
mess that introduces discoverability and a unified entrypoint.

```
# first you make a collection of little executables written in your
# preferred scripting language. you organize them into thematically
# consistent subdirectories

$ cd ~/foodops
$ ls
cook eat order
$ ./eat
nom nom

$ ls cook
boil braise fry
$ ./cook
$ ./cook/boil
bubble!
$ ./cook/fry
sizzle!

$ ls order
pizza random tacos thai
$ ./order/pizza
Who ordered a pizza?

# Here's how we will override Pushbutton magic with specially named files
# Let's write an ./order/.exec that hits the `random` subcommand
$ echo '#/bin/bash\
> $(dirname "${BASH_SOURCE[0]}")/random > ./order/.exec
$ ./order/.exec
I see you're feeling indecisive today. Randomly choosing: tacos!
Who ordered tacos?

# pushbutton gives you a command line interface with some nice magic
$ ./pushbutton.py foodops eat
nom nom
$ ./pushbutton.py foodops help
Subcommands: eat, cook, order
$ ./pushbotton.py foodops cook
You can cook: boil, braise, fry
$ ./pushbutton.py foodops cook all
bubble!
stew!
sizzle!
$ ./pushbutton.py foodops order
I see you're feeling indecisive today. Randomly choosing: thai!
Who ordered Thai?

# too much typing! make a shim!
$ ./make_pushbutton_shim.py foodops foodie
Installed pushbutton shim for ./foodops/ at /usr/local/bin/foodie
$ foodie cook boil
bubble!
$ foodie order
I see you're feeling indecisive today. Randomly choosing: pizza!
Who ordered pizza?
```

## Credit

Credit where credit is due: former coworker
https://github.com/kevinbirch came up with this general
tree-of-lil'-scripts-that-defines-command-line-interface pattern for
some great internal tooling we had at https://github.com/percolate.
