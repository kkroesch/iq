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
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import sqlite3

from console import success, warn, info, error

#
# CONFIG
#

from dotenv import load_dotenv
import os

load_dotenv()

#
# FUNCTIONS
#

def scrape_and_store(url, es_client):
    """ Extract document from web site. """

    """ Faking web browser """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code > 400:
            raise Exception("Unauthorized / Not found.")
        
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            'title': soup.title.string if soup.title else 'Kein Titel',
            #'description': soup.find("meta", {"name": "description"})["content"],
            #'keywords': soup.find("meta", {"name": "keywords"})["content"],
            'headings': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraphs': [p.text for p in soup.find_all('p')],
            'url': url,
            'last_seen': datetime.now().isoformat()
        }

        response = es_client.index(index='webdocuments', body=data)
        return response
    
    except Exception as e:
        error(f"Fehler beim Scrapen von {url}: {e}")


def indexed_url(url, search_id, conn):
    """ Store information for URL. """
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE websites
            (url, search_id, last_visited, last_indexed)
        VALUES
            ('{url}', '{search_id}', strftime('%s', 'now'), strftime('%s', 'now'))
        """)
    conn.commit()


def main():

    es = Elasticsearch(
        hosts=[os.getenv('ES_HOST', "https://localhost:9200")],
        http_auth=(os.getenv('ES_USER', "admin"), os.getenv('ES_PASSWORD', "admin")),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )

    if es.ping():
        success("Erfolgreich mit Elasticsearch verbunden!")
    else:
        error("Verbindung zu Elasticsearch fehlgeschlagen.")

    conn = sqlite3.connect('db/websites.db')
    cursor = conn.cursor()
    cursor.execute(""" SELECT url FROM websites """)
    for row in cursor:
        url = row[0]
        response = scrape_and_store(url, es)
        indexed_url(url, response.get('_id'), conn)


if __name__ == "__main__":
    main()
