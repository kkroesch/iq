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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            'title': soup.title.string if soup.title else 'Kein Titel',
            'headings': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraphs': [p.text for p in soup.find_all('p')],
            'url': url,
            'last_seen': datetime.now().isoformat()
        }

        es_client.index(index='webdocuments', body=data)
        print(f"Daten erfolgreich für {url} gespeichert")

    except Exception as e:
        print(f"Fehler beim Scrapen von {url}: {e}")


def main():

    es = Elasticsearch(
        hosts=[os.getenv('ES_HOST', "https://localhost:9200")],
        http_auth=(os.getenv('ES_USER', "admin"), os.getenv('ES_PASSWORD', "admin")),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )

    # Überprüfen Sie die Verbindung
    if es.ping():
        print("Erfolgreich mit Elasticsearch verbunden!")
    else:
        print("Verbindung zu Elasticsearch fehlgeschlagen.")

    # URLs aus der Datei 'bookmarks.txt' lesen und verarbeiten
    with open('bookmarks.txt', 'r') as file:
        for line in file:
            url = line.strip()
            scrape_and_store(url, es)


if __name__ == "__main__":
    main()
