======================
🎉 Git Precommit Hooks
======================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - 🔨 Code
      - | |black| |isort| |contributors| |commit| |license| |semver| |commits-since|
    * - 📝 Docs
      - | |gitmoji| |docformatter| |mypy| |docstyle| |gitchangelog|
    * - 🧪 Tests
      - | |github-actions| |pre-commit|

.. |black| image:: https://img.shields.io/badge/%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: The Uncompromising Code Formatter

.. |isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1
    :target: https://pycqa.github.io/isort/
    :alt: isort your imports, so you don't have to

.. |contributors| image:: https://img.shields.io/github/contributors/SterlingPeet/git-precommit-hooks
    :target: https://github.com/SterlingPeet/git-precommit-hooks/graphs/contributors
    :alt: Contributors to this project

.. |commit| image:: https://img.shields.io/github/last-commit/SterlingPeet/git-precommit-hooks

.. |license| image:: https://img.shields.io/badge/License-Apache_2.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache Software License 2.0

.. |semver| image:: https://img.shields.io/badge/Semantic%20Versioning-2.0.0-brightgreen.svg?style=flat
    :target: https://semver.org/
    :alt: Semantic Versioning - 2.0.0

.. |commits-since| image:: https://img.shields.io/github/commits-since/SterlingPeet/git-precommit-hooks/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/SterlingPeet/git-precommit-hooks/compare/v0.0.0...main

.. |gitmoji| image:: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg
    :target: https://github.com/carloscuesta/gitmoji
    :alt: Gitmoji Commit Messages

.. |docformatter| image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: Docformatter

.. |mypy| image:: https://img.shields.io/badge/types-Mypy-blue.svg
    :target: https://github.com/python/mypy
    :alt: Mypy

.. |docstyle| image:: https://img.shields.io/badge/%20style-google-3666d6.svg
    :target: https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings
    :alt: Documentation Style

.. |gitchangelog| image:: https://img.shields.io/badge/changes-gitchangelog-76b5c5
    :target: https://github.com/vaab/gitchangelog
    :alt: Changelog from Git Log

.. |github-actions| image:: https://github.com/SterlingPeet/git-precommit-hooks/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/SterlingPeet/git-precommit-hooks/actions

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. end-badges

Some additional pre-commit hooks, patterned after the `pre-commit-hooks`_ project.

🚀 Using ``pre-commit-hooks`` with ``pre-commit``
=================================================

Add this to your ``.pre-commit-config.yaml``

.. code-block:: yaml

  - repo: https://github.com/SterlingPeet/git-precommit-hooks
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
    - id: check-git-hooks-installed
    # - id: other-hook-you-want-to-use


📝 Hooks Available
==================

``check-git-hooks-installed``
-----------------------------

Ensure that ``pre-commit`` is installed for all of the expected hooks.

- Specify when this hook runs using the ``stages`` key.
- Use ``--hook`` argument to specify the hook(s) you want to check for.

.. code-block:: yaml

  - repo: ../git-precommit-hooks
    rev: b58d47c6a5
    hooks:
    - id: check-git-hooks-installed
      stages: [pre-commit, pre-merge-commit, pre-push, commit-msg]
      args: [--hook, 'pre-commit,commit-msg,pre-push']


You can use the following config keys in ``.pre-commit-config.yaml`` to help users automatically install the hooks:

.. code-block:: yaml

  default_install_hook_types: [pre-commit, pre-merge-commit, pre-push, commit-msg]
  default_stages: [pre-commit, pre-merge-commit, pre-push, commit-msg]

.. note::

  This requires an up to date version of ``pre-commit``.  Versions before
  ``v3.0.0`` have breaking changes in the config schema.


.. _pre-commit-hooks: https://github.com/pre-commit/pre-commit-hooks
