# -*- mode: python ;
# coding: utf-8 -*-
import sys

from src.cli.commands import main as cli_main

def main() -> None:
    cli_main()

if __name__ == "__main__":
    # sys.argv = ['__main__.py', 'create-project', 'Estructura Documental de Empresa 1']
    # main()
    sys.argv = ['__main__.py','create-project', 'Estructura Documental', '--force']
    main()