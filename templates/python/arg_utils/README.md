Argument Utils
==============

If it is not clear enough, you can extrapolate the source code functionality 
from this shell output.

```
$ ./arg_utils.py -h
usage: arg_utils.py [-h] [-a1 FIRST_OPT_ARG] [--version]
                    first_mandatory_arg {subcommand1} ...

This is a generic code to handle parameters with the argparse python library.
It shows how to use the most useful options of the package.

positional arguments:
  first_mandatory_arg   First mandatory argument
  {subcommand1}         Several subcommands available
    subcommand1         Help for the subcommand1

optional arguments:
  -h, --help            show this help message and exit
  -a1 FIRST_OPT_ARG, --first_opt_arg FIRST_OPT_ARG
                        First optional argument (default: value1)
  --version             show program's version number and exit

Coded by newlog.

$ ./arg_utils.py 1 -a1 value2 subcommand1 mand2 -a2 opt2.1 opt2.3 opt2.3 -vv
Namespace(first_mandatory_arg=1, first_opt_arg=['value2'], second_mandatory_arg='mand2', second_opt_arg=['opt2.1', 'opt2.3', 'opt2.3'], v=2)
First mand. argument value: 1
Second mand. argument value: mand2
First opt. argument value: ['value2']
Second opt. argument value: ['opt2.1', 'opt2.3', 'opt2.3']
Verbosity count = 2
Beleriand-2:arg_utils newlog$ ./arg_utils.py --version
arg_utils.py 2.0
```
