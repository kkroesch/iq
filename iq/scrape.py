#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#
# IMPORTS
#

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from console import console, success, warn, info, error
import sqlite3

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
            #'description': soup.find("meta", {"name": "description"}).get("content", 'N/A'),
            #'keywords': soup.find("meta", {"name": "keywords"}).get("content", 'N/A'),
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
    cursor.execute("""
        UPDATE websites
            (url, search_id, last_visited, last_indexed)
        VALUES
            (?, ?, ?, ?)
        """, (url, search_id, datetime.now(), datetime.now()))
    conn.commit()


def categorize(text, model_name="bert-base-uncased"):
    classifier = pipeline("text-classification", model=model_name)
    result = classifier(text)
    return result


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
