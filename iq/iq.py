#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TOOL_NAME="iq"
TOOL_VERSION="0.1"
TOOL_VERBOSE_NAME="iQ Tool to import data and control iQ crawler component."

"""
Dateiname: iq.py
Autor: Karsten Kroesch

Beschreibung: 
Importiert Bookmarks aus Chrome, Brave, Github Stars, Linktr.ee, Youtube in die Crawler-Datenbank
und steuert den Crawl-Durchlauf.

Lizenz: MIT
"""


#
# IMPORTS
#

from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup as bs4
from elasticsearch import Elasticsearch

from console import console, success, warn, info, error
from rich.table import Table
from scrape import scrape_and_store

#
# CONFIG
#

from dotenv import load_dotenv
import argparse
import os

es = Elasticsearch(
    hosts=[os.getenv('ES_HOST', "https://localhost:9200")],
    http_auth=(os.getenv('ES_USER', "admin"), os.getenv('ES_PASSWORD', "admin")),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
)


#
# FUNCTIONS
#

def init_database(args, conn, console):
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY,
            title TEXT NULL,
            url TEXT NOT NULL,
            search_id TEXT NULL,
            category TEXT NULL,rm 
            last_visited INTEGER NULL,
            status_code INTEGER NULL,
            last_indexed INTEGER NULL
        )
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        sql = "CREATE UNIQUE INDEX unique_url ON websites(url)"
        cursor.execute(sql)
    except Exception as ex:
        error(ex)


def import_bookmarks(args, conn, console):
    cursor = conn.cursor()
    with open(args.filename, 'r') as file:
        content = bs4(file.read(), 'html.parser')
        
        for link in content.find_all('a'):
            title = link.text
            url = link.get('href')
            add_date = link.get('add_date')
            if args.markdown:
                print(f"  - [{title}]({url})")
                continue
            try:
                cursor.execute('INSERT INTO websites (title, url, last_visited) VALUES (?, ?, ?)', 
                (title, url, add_date))
            except Exception as ex:
                warn(f"Ignoring {url}: {ex}")
            finally:
                conn.commit()


def list_websites(args, conn, console):
    """ List all stored bookmarks. """
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM websites """)
    
    table = Table(title="Beispieltabelle")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("URL", style="green")

    for row in cursor:
        table.add_row(str(row[0]), row[1], row[2])

    console.print(table)


def crawl_websites(args, conn, console):
    """ Crawl stored bookmarks. """
    cursor = conn.cursor()
    cursor.execute(""" SELECT url FROM websites """)

    for row in cursor:
        url = row[0]
        info(f"Scraping {url}...")
        scrape_and_store(url, es)


#
# ACTIONS
#

class CrawlAction(argparse.Action):
    """ Crawl websites from database. """
    def __init__(self, conn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = conn
    
    def __call__(self, parser, namespace, values, option_string=None):
        cursor = self.conn.cursor()
        cursor.execute(""" SELECT * FROM websites """)
        for row in cursor:
            print(f"Crawling {row['url']}")

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
    conn = sqlite3.connect(os.getenv('DB_FILE', 'db/websites.db'))

    parser = argparse.ArgumentParser(
        description=TOOL_VERBOSE_NAME,
        epilog="Copyright 2024 by Karsten Kroesch. MIT License.")
    parser.add_argument("--version", action="version", version=' '.join((TOOL_NAME, TOOL_VERSION)))

    subparsers = parser.add_subparsers()
    parser_init = subparsers.add_parser('init',
        help="Initilisiert Datenbank und Konfiguration.")
    parser_init.set_defaults(func=init_database)

    parser_extract = subparsers.add_parser('import', 
        help="Extrahiert aus einer Bookmark-Datei URLs.")
    parser_extract.add_argument('-f', '--filename', 
        help='Dateiname (default: Bookmarks)')
    parser_extract.add_argument('-t', '--title', action='store_true', 
        help='Extrahiert den Titel der Webiste (online).')
    parser_extract.add_argument('-m', '--markdown', action='store_true', 
        help='Gibt Bookmarks im Markdown-Format aus.')
    parser_extract.add_argument('--github-user',
        help='Extrahiert Favoriten aus Github-Favoriten.')
    parser_extract.add_argument('--youtube-channel',
        help='Extrahiert Playlists aus Youtube.')
    parser_extract.set_defaults(func=import_bookmarks)

    parser_scrape = subparsers.add_parser('crawl', 
        help="Besucht Websites und speichert Inhalte in Suchindex.")
    parser_scrape.add_argument('--resume', action=CrawlAction, conn=conn, nargs='+',
        help="Setzt den Vorgang an der zuletzt unterbrochenen Stelle fort.")
    parser_scrape.set_defaults(func=crawl_websites)

    parser_list = subparsers.add_parser('list', aliases=['ls'],
        help="Listet gespeicherte Websites.")
    parser_list.set_defaults(func=list_websites)

    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args, conn, console)
    else:
        parser.print_help()

    conn.close()


if __name__ == "__main__":
    main()
