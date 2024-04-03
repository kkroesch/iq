package main

import (
	"encoding/json"
	"fmt"

	"github.com/vanng822/go-solr/solr"
)

type SolrDocument struct {
	Body        []string `json:"body"`
	Title       string   `json:"title"`
	Description string   `json:"description"`
	Last_seen   string   `json:"last_seen"`
	Url         string   `json:"url"`
}

// Fügt ein Dokument zu Solr hinzu, basierend auf einem JSON-String
func AddDocumentToSolr(solrURL string, coreName string, jsonDoc string) error {
	// JSON-String in ein SolrDocument-Struct umwandeln
	var doc SolrDocument
	if err := json.Unmarshal([]byte(jsonDoc), &doc); err != nil {
		return fmt.Errorf("error parsing JSON document: %v", err)
	}

	// Verbindung zum Solr-Server herstellen
	s, err := solr.NewSolrInterface(solrURL, coreName)
	if err != nil {
		return fmt.Errorf("cannot connect to Solr: %v", err)
	}

	// Dokument zu Solr hinzufügen
	update := map[string]interface{}{
		"add": map[string]interface{}{
			"doc": doc,
		},
	}
	_, err = s.Update(update, nil)
	if err != nil {
		return fmt.Errorf("error storing document: %v", err)
	}
	return nil
}
