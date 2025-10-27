# -*- mode: python ; coding: utf-8 -*-
import sys

from src.cli.commands import main as cli_main

def main() -> None:
    cli_main()

if __name__ == "__main__":
    sys.argv += ['create-project', "Operadoras"]
    main()