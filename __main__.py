# -*- mode: python ;
# coding: utf-8 -*-
import shutil
import sys

from src.cli.commands import main as cli_main


def main() -> None:
    cli_main()


if __name__ == "__main__":
    name_test = 'Estructura Demo'
    # shutil.rmtree(name_test, ignore_errors=True)
    #
    # db = 'project-manager.db'
    # shutil.rmtree(db, ignore_errors=True)

    sys.argv = ['__main__.py', 'create-project', name_test,'--format', 'img', '--force']
    main()
