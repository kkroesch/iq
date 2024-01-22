/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"fmt"
	"log"
	"net/http"

	"github.com/PuerkitoBio/goquery"
	"github.com/spf13/cobra"
)

var (
	siteUrl string
)

type Website struct {
	Url         string
	Title       string
	Description string
	Keywords    []string
	Content     []string
}

func crawl(url string) {
	res, err := http.Get(url)
	if err != nil {
		log.Fatalf("Error getting URL %s: %s", url, err)
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		log.Fatalf("Unhealthy Status: %d %s", res.StatusCode, res.Status)
	}

	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal("Error loading document:", err)
	}

	doc.Find("head").Find("title, description, keywords").Each(func(i int, s *goquery.Selection) {
		text := s.Text()
		fmt.Printf("Metadaten gefunden: %s\n", text)
	})

	// Durchlaufe alle <article> und <p>-Tags im <body> und extrahiere den Text
	doc.Find("body").Find("article, p, article div").Each(func(i int, s *goquery.Selection) {
		text := s.Text()
		fmt.Printf("Text gefunden: %s\n", text)
	})

}

var crawlCmd = &cobra.Command{
	Use:   "crawl",
	Short: "Crawl text from website and index.",
	Long:  `Crawls a single website (requires --url) or all sites from database and stores the text in index for later search. The status of the visited site is added to the default database.`,
	Run: func(cmd *cobra.Command, args []string) {
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
}
