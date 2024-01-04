#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TOOL_NAME="example_tool"
TOOL_VERSION="0.1"
TOOL_VERBOSE_NAME="Example Tool with Colors"

"""
Dateiname: mein_skript.py
Autor: Dein Name

Beschreibung: 
Dieses Skript führt [eine bestimmte Aufgabe] aus. Es nutzt [bestimmte Bibliotheken oder Frameworks]
und ist Teil des Projekts [Projektname]. Dieses Skript demonstriert [spezifische Konzepte oder Techniken].
Es ist abhängig von [Abhängigkeiten, falls vorhanden] und nutzt Daten von [Datenquellen, falls zutreffend].

Verwendung: 
Führen Sie das Skript aus der Kommandozeile wie folgt aus: 
python mein_skript.py [Optionale Argumente]

Lizenz: MIT
"""


#
# IMPORTS
#

from datetime import datetime
import sqlite3

from console import console, success, warn, info, error
from rich.table import Table


#
# CONFIG
#

from dotenv import load_dotenv
import argparse
import os


#
# FUNCTIONS
#

def list_websites(args, conn, console):
    """ Extract document from web site. """
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM websites """)
    
    table = Table(title="Beispieltabelle")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("URL", style="green")

    for row in cursor:
        table.add_row(str(row[0]), row[1], row[2])

    console.print(table)

#
# ACTIONS
#

class FooAction(argparse.Action):
    """ Example action """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, values)

#
# MISC
#

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


#
# MAIN
#

def main():
    """ Main method -- pass all initialized connections to function calls. """
    load_dotenv()

    parser = argparse.ArgumentParser(
        description=TOOL_VERBOSE_NAME,
        epilog="Dieses Tool hat keine Super-Kuh-Kräfte.")
    parser.add_argument("--version", action="version", version=' '.join((TOOL_NAME, TOOL_VERSION)))

    subparsers = parser.add_subparsers()
    parser_extract = subparsers.add_parser('extract', 
        help="Extrahiert aus einer Bookmark-Datei URLs.")
    parser_extract.add_argument('--filename', 
        help='Dateiname (default: Bookmarks)')
    parser_extract.add_argument('-t', action='store_true', 
        help='Extrahiert den Titel der Webiste (online).')

    parser_scrape = subparsers.add_parser('scrape', 
        help="Besucht Websites und speichert Inhalte in Suchindex.")
    parser_scrape.add_argument('--resume', 
        help="Setzt den Vorgang an der zuletzt unterbrochenen Stelle fort.")

    parser_list = subparsers.add_parser('list', aliases=['ls'],
        help="Listet gespeicherte Websites.")
    parser_list.set_defaults(func=list_websites)

    args = parser.parse_args()

    conn = sqlite3.connect(os.getenv('DB_FILE', 'db/websites.db'))
    
    if hasattr(args, 'func'):
        args.func(args, conn, console)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
