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

	_ "github.com/mattn/go-sqlite3"
)

var (
	filePath string
	dbPath   string
)

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

		db, err := sql.Open("sqlite3", dbPath)
		if err != nil {
			log.Fatal("Error opening database: ", err)
		}
		defer db.Close()

		counter := 0

		doc.Find("a").Each(func(i int, s *goquery.Selection) {
			title := s.Text()
			url, exists := s.Attr("href")
			if !exists {
				return
			}

			stmt, err := db.Prepare(`
				INSERT INTO websites 
				(title, url)
				VALUES
				(?, ?)
				ON CONFLICT (url)
				DO UPDATE SET last_visited = strftime('%s', 'now');
			`)
			if err != nil {
				log.Fatal("Error preparing SQL: ", err)
			}
			defer stmt.Close()

			_, err = stmt.Exec(title, url)
			if err != nil {
				log.Fatal("DB error: ", err)
			} else {
				counter++
			}
		})
		log.Printf("Imported %d URLs into websites database.\n", counter)
	},
}

func init() {
	rootCmd.AddCommand(importCmd)
	importCmd.PersistentFlags().StringVarP(&filePath, "file", "f", "bookmark.html", "Path to your bookmark file.")
	importCmd.PersistentFlags().StringVarP(&dbPath, "database", "d", "./websites.db", "Path to the websites database.")
}
