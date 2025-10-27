# -*- mode: python ; coding: utf-8 -*-

from .src.cli.commands import main as cli_main

def main() -> None:
    cli_main()

if __name__ == "__main__":
    main()