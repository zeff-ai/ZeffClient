**************************
Contributing to ZeffClient
**************************

Thank you for taking the time to contribute!

This contains guidlines for contributing to ZeffClient. Mostly these are
strong recommendations, but not rules. Feel free to propose changes to
this document with a pull request.


.. contents::


Code of Conduct
===============

That which is hateful to you, do not do to your neighbor (Hillel the Elder).


How Can I Contribute?
=====================

Reporting Bugs
--------------

Bug reports may be made in the project's
`issue <https://github.com/zeff.ai/ZeffClient/issues>`_ page.


Suggesting Enhancements
-----------------------

Enhangement requests may be made in the project's
`issue <https://github.com/zeff.ai/ZeffClient/issues>`_ page.


Pull Requests
-------------

#. ``make validate``

   - Should be executed before any commit is created.
   - Continuous integration will execute this command on any pull request.
   - Continuous integration will reject a pull request that fails.



Styleguides
===========


Git Commit Messages
-------------------

- Use present tense (e.g. "Add fubar" not "Added fubar").

- Use imperative mood (e.g. "Move cursor to…" not "Moves cursor to…").

- Limit the first line to 72 characters or less.

- Reference issues and pull requests after the first line (e.g. "fixes #1234").

- Start commit message with an applicable emoji:

  =============== =======
  Commit Type      Emoji
  =============== =======
  Release            🚀
  Feature            📦
  Bugfix             🐛
  Documentation      📚
  Code Structure     🎨
  =============== =======



Python Styleguide
-----------------

- Python source must adhere to `PEP 8 -- Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_.

  - ``make validate`` executes ``pylint`` and ``pycodestyle`` to aid in following PEP 8.

- Code formatting shall be performed with `Black: The uncompromising Python code formatter <https://github.com/psf/black>`_.

  - ``make validate`` executes Black on all Python files in the project.



Documentation Styleguide
------------------------

- Use `reStructuredText <https://docutils.sourceforge.io/rst.html>`_.

- Python source:

  - Follow `PEP 257 -- Docstring Conventions <https://www.python.org/dev/peps/pep-0257/>`_.

  - Follow `PEP 287 -- reStructuredText Docstring Format <https://www.python.org/dev/peps/pep-0287/>`_.

  - Follow `Sphinx reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ documentation style.



Additional Notes
================



