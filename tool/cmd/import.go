/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"database/sql"
	"log"
	"os"

	"github.com/PuerkitoBio/goquery"
	"github.com/spf13/cobra"

	_ "github.com/lib/pq"
)

var (
	filePath string
	connStr  string
	conn     *sql.DB
)

func storeUrl(title, url string) bool {
	// INSERT-Statement vorbereiten
	query := `
	INSERT INTO websites (title, url)
	VALUES ($1, $2)
	ON CONFLICT (url)
	DO UPDATE SET last_visited = EXTRACT(EPOCH FROM NOW());
	`
	// INSERT-Statement ausführen
	_, err := conn.Exec(query, title, url)
	if err != nil {
		log.Fatal(err)
		return false
	} else {
		return true
	}
}

// importCmd represents the import command
var importCmd = &cobra.Command{
	Use:   "import",
	Short: "Import bookmark file into database.",
	Long:  `Import URLs and names from bookmark.html file into crawl database.`,
	Run: func(cmd *cobra.Command, args []string) {
		file, err := os.Open(filePath)
		if err != nil {
			log.Fatal("Error opening bookmark file:", err)
		}
		defer file.Close()

		doc, err := goquery.NewDocumentFromReader(file)
		if err != nil {
			log.Fatal("Error reading HTML:", err)
		}

		counter := 0

		doc.Find("a").Each(func(i int, s *goquery.Selection) {
			title := s.Text()
			url, exists := s.Attr("href")
			if !exists {
				return
			}
			storeUrl(title, url)
			counter++
		})
		log.Printf("Imported %d URLs into websites database.\n", counter)
	},
}

func init() {
	rootCmd.AddCommand(importCmd)
	importCmd.PersistentFlags().StringVarP(&filePath, "file", "f", "bookmark.html", "Path to your bookmark file.")
	//importCmd.PersistentFlags().StringVarP(&dbPath, "database", "d", "./websites.db", "Path to the websites database.")

	connStr = os.Getenv("POSTGRES_CONNECTION_URL")
	// "postgres://username:password@host:port/dbname?sslmode=disable"
	conn, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
}
