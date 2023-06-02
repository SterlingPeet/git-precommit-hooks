"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mgit_precommit_hooks` python will execute
    ``__main__.py`` as a script. That means there will not be any
    ``git_precommit_hooks.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there"s no ``git_precommit_hooks.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import os
from typing import Sequence

parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument(
    'names',
    metavar='NAME',
    nargs=argparse.ZERO_OR_MORE,
    help='A name of something.',
)


def main(args: Sequence[str] | None = None) -> int:
    args = parser.parse_args(args=args)
    print(args.names)

    value = os.getenv('GIT_DIR')

    if value is not None:
        print(f'The value of MY_VARIABLE is: {value}')
    else:
        print('MY_VARIABLE is not set.')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
