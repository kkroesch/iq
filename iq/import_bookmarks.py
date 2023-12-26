#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

#
# CONFIG
#

from dotenv import load_dotenv
import os

load_dotenv()

#
# FUNCTIONS
#

def add_url(url, conn):
    """ Write URLs into database. """
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO websites 
            (url)
        VALUES
            (?)
        ON CONFLICT (url)
        DO UPDATE SET last_visited = strftime('%s', 'now');
        """, (url))
    conn.commit()


def main():
    conn = sqlite3.connect(os.getenv('WEB_DB', 'db/websites.db'))
    with open('test/fixtures/bookmarks.txt', 'r') as file:
        for line in file:
            url = line.strip()
            add_url(url, conn)


if __name__ == "__main__":
    main()
