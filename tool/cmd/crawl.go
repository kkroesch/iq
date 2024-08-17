/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"log"
	"net/http"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/spf13/cobra"
)

var (
	siteUrl     string
	synchronize bool
)

type Website struct {
	Url         string
	Title       string
	Description string
	Keywords    []string
	Content     []string
}

func crawl(url string) {
	headers := map[string]string{
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	}

	// HTTP-Request mit benutzerdefinierten Headern
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		panic(err)
	}
	for key, value := range headers {
		req.Header.Add(key, value)
	}

	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode > 400 {
		panic("Unauthorized / Not found.")
	}

	// HTML parsen
	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		panic(err)
	}

	title := "Kein Titel"
	if doc.Find("title").Length() > 0 {
		title = doc.Find("title").Text()
	}

	var chunks []string
	doc.Find("h1, h2, h3, article, p, article div").Each(func(i int, s *goquery.Selection) {
		chunks = append(chunks, s.Text())
	})

	document := SolrDocument{
		Title:     title,
		Body:      chunks,
		Url:       url,
		Last_seen: time.Now().Format(time.RFC3339),
	}

	AddDocumentToSolr("http://localhost:8983/solr", "websites", document)
}

func synchronizeWitdhDb() {

}

var crawlCmd = &cobra.Command{
	Use:   "crawl",
	Short: "Crawl text from website and index.",
	Long:  `Crawls a single website (requires --url) or all sites from database and stores the text in index for later search. The status of the visited site is added to the default database.`,
	Run: func(cmd *cobra.Command, args []string) {
		if synchronize {
			synchronizeWitdhDb()
			return
		}

		if siteUrl == "" {
			log.Fatal("Empty URL.")
		} else {
			crawl(siteUrl)
		}
	},
}

func init() {
	rootCmd.AddCommand(crawlCmd)
	crawlCmd.PersistentFlags().StringVarP(&siteUrl, "url", "u", "", "URL to visit.")
	crawlCmd.PersistentFlags().BoolVarP(&synchronize, "synchronize", "s", false, "Synchronize with database.")
}
