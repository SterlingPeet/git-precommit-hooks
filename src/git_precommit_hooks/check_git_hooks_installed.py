"""
Check the git repository hook scripts for valid hook installations.
"""
import argparse
import os
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Sequence

import git

parser = argparse.ArgumentParser(
    description='Check git repository for installed hooks.'
)
parser.add_argument(
    '-p',
    '--path',
    default=Path.cwd(),
    help='git repository location (default cwd)',
)
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='increase verbosity for debugging',
)
parser.add_argument(
    '--hooks',
    default='pre-commit',
    help='comma separated, no spaces list of hook names to check',
)
parser.add_argument(
    'names',
    metavar='FILENAME',
    nargs=argparse.ZERO_OR_MORE,
    help='a name of an edited file to check (unused)',
)


def get_hook_path(hook_name: str, repo_path: Path):
    """Collect path to hook from hook name and repository path."""
    repo = git.Repo(path=repo_path, search_parent_directories=True)
    return Path(git.index.fun.hook_path(hook_name, repo.git_dir))


def check_hook_shebang(hook_path: Path) -> bool:
    """ "Check the first line in the file for shebang."""
    first_line = ''
    with hook_path.open() as fh:
        first_line = fh.readline().strip()
    return first_line.startswith('#!/')


class VerbosePrint:
    """Print if the verbose state is True."""

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        if self.verbose:
            print(*args, **kwargs)


def main(sys_args: Optional[Sequence[str]] = None) -> int:
    args = parser.parse_args(args=sys_args)
    print(sys_args)
    flag = 0
    hook_list = []
    v_print = VerbosePrint(args.verbose)

    for hook in args.hooks.split(','):
        hook_list.append(hook)

    v_print(f'Requested hook list: {hook_list}')
    v_print(f'Checking hooks within {args.path}')

    for hook in hook_list:
        continue_checks = True
        hook_path = get_hook_path(hook, args.path)

        # Test for file existence
        if hook_path.is_file():
            v_print(f' ✅ {hook} hook is present at: {hook_path}')
        else:
            print(f' ❌ {hook} hook is not found in the repository.')
            continue_checks = False
            flag += 1

        # If file exists, test for executable bit
        if continue_checks and not os.access(hook_path, os.X_OK):
            print(f' ❌ {hook} hook is not executable.')
            continue_checks = False
            flag += 1

        # If file is executeable, test for #!/
        if continue_checks and not check_hook_shebang(hook_path):
            print(
                f' ❌ {hook} hook does not contain "#!/" executable definition.'
            )
            flag += 1

    if flag > 0:
        print('To install hooks, run: pre-commit install')

    return flag


if __name__ == '__main__':
    raise SystemExit(main())
