import pydoc

from makefile_help import help_from_makefile


def main():
    makefile_help = help_from_makefile()
    pydoc.pipepager(makefile_help, cmd='less -R')


if __name__ == "__main__":
    main()
