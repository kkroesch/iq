package cmd

import (
	"testing"
)

func TestAddDocumentToSolr(t *testing.T) {
	solrURL := "http://localhost:8983/solr" // Ändere dies entsprechend deiner Solr-Server-URL
	coreName := "websites"
	jsonDoc := SolrDocument{
		Body: []string{
			"Kubernetes",
			"This article or section needs language, wiki syntax or style improvements. See Help:Style for reference.",
			"Kubernetes (aka. k8s) is an open-source system for automating the deployment, scaling, and management of containerized applications.\n",
			"Installation",
			"There are many methods to setup a kubernetes cluster. This article will focus on bootstrapping with kubeadm.\n",
			"Deployment tools",
			"You may have forgotten to choose systemd cgroup driver. See this GitHub issue reporting this.\n",
		},
		Last_seen: "2024-04-02T17:06:19+02:00",
		Title:     "Kubernetes - ArchWiki",
		Url:       "https://wiki.archlinux.org/title/Kubernetes",
	}

	// Führe die Funktion aus, die getestet werden soll
	err := AddDocumentToSolr(solrURL, coreName, jsonDoc)
	if err != nil {
		t.Fatalf("Fehler beim Hinzufügen des Dokuments zu Solr: %v", err)
	}

	// Hier würdest Du normalerweise Überprüfungen durchführen, um sicherzustellen, dass das Dokument
	// korrekt hinzugefügt wurde. Da dies einen realen Solr-Server erfordert, ist es für dieses Beispiel
	// schwierig, ohne ein Mocking-Framework.
}
