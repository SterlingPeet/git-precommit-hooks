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

standard_hook_list = [
    'pre-commit',
    'prepare-commit-msg',
    'commit-msg',
    'post-commit',
    'pre-rebase',
    'post-rewrite',
    'post-checkout',
    'post-merge',
    'pre-push',
    'pre-auto-gc',
    'pre-recieve',
    'update',
    'post-recieve',
]

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
    '--list-standard-hooks',
    action='store_true',
    help='print out the list of standard supported hooks',
)
parser.add_argument(
    '--hook',
    metavar='HOOK',
    choices=standard_hook_list,
    nargs='*',
    help='a hook name to check (ommision will check pre-commit)',
)
parser.add_argument(
    '--custom-hook',
    metavar='HOOK',
    nargs='*',
    help='custom hook name to check',
)
parser.add_argument(
    'names',
    metavar='FILENAME',
    nargs=argparse.ZERO_OR_MORE,
    help='a name of an edited file to check (unused)',
)


def print_standard_hooks() -> None:
    """Print the standard hooks to the console."""
    print('\nThese are the hooks supported by the --hook option:\n')
    for hook in standard_hook_list:
        print(f' - {hook}')
    print('\nMultiple values can be given in the same cli invocation:\n')
    print(' --hook pre-commit post-commit\n')


def get_hook_path(hook_name: str, repo_path: Path):
    """Collect path to hook from hook name and repository path."""
    repo = git.Repo(search_parent_directories=True)
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

    if args.list_standard_hooks:
        print_standard_hooks()
        return 0

    flag = 0
    hook_list = []
    v_print = VerbosePrint(args.verbose)

    # Set default hook if none provided
    if args.hook is None:
        hook_list.append('pre-commit')
    else:
        # Add all hooks specified on the command line
        for hook in args.hook:
            hook_list.append(hook)

    # print(hook_list)

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

    return flag


if __name__ == '__main__':
    raise SystemExit(main())
