from unittest import mock

import makefile_help


def test_help_from_makefile():
    read_data = """help: # Display help and exit
	python -m makefile_help

install: # Install package using poetry
	poetry install

test: # Run pytest in poetry environment
	poetry run pytest

clean: # Remove .pyc, .pyo, __pycache__ dirs
	find . -type f -name '*.py[co]' -delete -o \
		-type d -name __pycache__ -delete"""
    mock_open = mock.mock_open(read_data=read_data)
    expected_result = """
\x1b[31mMakefile help

\x1b[33mTo see command run: \x1b[36m
   $ make -n <command-name>

\x1b[33mCommands:

\x1b[32mhelp........\x1b[36mDisplay help and exit
\x1b[32minstall.....\x1b[36mInstall package using poetry
\x1b[32mtest........\x1b[36mRun pytest in poetry environment
\x1b[32mclean.......\x1b[36mRemove .pyc, .pyo, __pycache__ dirs

\x1b[39m"""
    with mock.patch('builtins.open', mock_open):
        generated_help = makefile_help.help_from_makefile()
        assert generated_help == expected_result


def test_help_from_makefile_with_sections():
    read_data = """help: # @@Utils@@ Display help and exit
	python -m makefile_help

clean: # @@Utils@@ Remove .pyc, .pyo, __pycache__ dirs
	find . -type f -name '*.py[co]' -delete -o \
		-type d -name __pycache__ -delete

install: # @@Python@@ Install package using poetry
	poetry install

test: # @@Python@@ Run pytest in poetry environment
	poetry run pytest -vvs"""
    mock_open = mock.mock_open(read_data=read_data)
    expected_result = """
\x1b[31mMakefile help

\x1b[33mTo see command run: \x1b[36m
   $ make -n <command-name>

\x1b[33mCommands:

\x1b[90mUtils:
\x1b[32mhelp........\x1b[36mDisplay help and exit
\x1b[32mclean.......\x1b[36mRemove .pyc, .pyo, __pycache__ dirs

\x1b[39m\x1b[90mPython:
\x1b[32minstall.....\x1b[36mInstall package using poetry
\x1b[32mtest........\x1b[36mRun pytest in poetry environment

\x1b[39m"""
    with mock.patch('builtins.open', mock_open):
        generated_help = makefile_help.help_from_makefile()
        assert generated_help == expected_result


def test_wrap_desc():
    expected = 'this description\n\x1b[36m               is 33 chars long'
    desc = "this description is 33 chars long"
    command_max = 10
    makefile_help.MAX_LINE_LENGTH = 31
    wrapped_desc = makefile_help.wrap_desc(desc, command_max)
    assert expected == wrapped_desc


def test_wrap_desc_multiple():
    expected = (
        'this\n'
        '\x1b[36m               description is\n'
        '\x1b[36m               33 chars long')
    desc = "this description is 33 chars long"
    command_max = 10
    makefile_help.MAX_LINE_LENGTH = 30
    wrapped_desc = makefile_help.wrap_desc(desc, command_max)
    assert expected == wrapped_desc
