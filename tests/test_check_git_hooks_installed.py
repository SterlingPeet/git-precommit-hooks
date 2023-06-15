from pathlib import Path

import pytest
from git import Repo

from git_precommit_hooks.check_git_hooks_installed import check_hook_shebang
from git_precommit_hooks.check_git_hooks_installed import main


@pytest.fixture
def git_repository(tmpdir):
    # Create a temporary directory
    temp_dir = Path(tmpdir)

    # Initialize a Git repository
    repo_path = temp_dir.joinpath('my_repo')
    repo = Repo.init(repo_path)

    # Perform some initial commits for testing
    with Path.open(repo_path.joinpath('file1.txt'), 'w') as f:
        f.write('Content 1')
    repo.index.add(['file1.txt'])
    repo.index.commit('Initial commit')

    with Path.open(repo_path.joinpath('file2.txt'), 'w') as f:
        f.write('Content 2')
    repo.index.add(['file2.txt'])
    repo.index.commit('Second commit')

    # Add a valid pre-commit hook
    hooks_path = repo_path.joinpath('.git/hooks')
    hook_path = hooks_path.joinpath('pre-commit')
    with Path.open(hook_path, 'w') as fh:
        fh.write('#!/bin/bash\n')
        fh.write("echo 'Running pre-commit hook'")
        fh.write('\nexit 0')  # Dummy hook that always succeeds

    # Make the hook file executable
    hook_path.chmod(0o755)

    # Add an executable post-commit hook with no shebang
    hook_path = hooks_path.joinpath('post-commit')
    hook_path.touch()

    # Make the hook file executable
    hook_path.chmod(0o755)
    hook_path = hooks_path.joinpath('update')
    hook_path.touch()

    # Add a non-executable update hook

    # Provide the repository object as a fixture
    yield repo

    # Clean up the temporary directory after each test
    repo.close()


def test_basic_hook_present(git_repository):
    assert main(['--path', git_repository.working_dir]) == 0


def test_check_hook_shebang_true(git_repository):
    repo_path = Path(git_repository.working_dir)
    test_file = repo_path.joinpath('.git/hooks/pre-commit')
    assert check_hook_shebang(test_file) is True


def test_check_hook_shebang_false(git_repository):
    repo_path = Path(git_repository.working_dir)
    test_file = repo_path.joinpath('.git/hooks/post-commit')
    assert check_hook_shebang(test_file) is False


def test_three_bad_hooks(git_repository):
    assert (
        main(
            [
                '--path',
                git_repository.working_dir,
                '--verbose',
                '--hooks',
                'pre-commit,post-commit,update,commit-msg',
            ]
        )
        == 3
    )


# def test_another_commit_count(git_repository):
#     # Add another commit
#     repo_path = Path(git_repository.working_dir)
#     with Path.open(repo_path.joinpath('file3.txt'), 'w') as f:
#         f.write('Content 3')
#     git_repository.index.add(['file3.txt'])
#     git_repository.index.commit('Third commit')

#     assert len(list(git_repository.iter_commits())) == 3
