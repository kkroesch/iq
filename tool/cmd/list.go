/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"strconv"
	"text/tabwriter"
	"unicode/utf8"

	_ "github.com/mattn/go-sqlite3"
	"github.com/spf13/cobra"
)

// TruncateString kürzt einen String auf eine maximale Länge
// und fügt ein Auslassungszeichen hinzu, falls erforderlich
func TruncateString(s string, maxLength int) string {
	if maxLength <= 0 {
		return ""
	}
	if utf8.RuneCountInString(s) > maxLength {
		return s[:maxLength-1] + "…"
	}
	return s
}

// listCmd represents the list command
var listCmd = &cobra.Command{
	Use:   "list",
	Short: "Shows the content of the bookmark database",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		db, err := sql.Open("sqlite3", "../db/websites.db")
		if err != nil {
			log.Fatal(err)
		}
		defer db.Close()
		rows, sql_err := db.Query("SELECT id, title, url FROM websites")
		if sql_err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		writer := tabwriter.NewWriter(os.Stdout, 0, 0, 1, ' ', 0)

		// Kopfzeilen
		fmt.Fprintln(writer, "Id\ttitle\tURL\t")
		fmt.Fprintln(writer, "----\t-------------------------------------\t------------------------------\t")

		for rows.Next() {
			var id, url string
			var title sql.NullString
			err = rows.Scan(&id, &title, &url)
			if err != nil {
				log.Fatal(err)
			}
			titleValue := ""
			if title.Valid {
				titleValue = title.String
			}
			iid, typeErr := strconv.Atoi(id)
			if typeErr == nil {
				id = fmt.Sprintf("%4d", iid)
			}
			fmt.Fprintf(writer, "%s\t%s\t%s\t\n", id, TruncateString(titleValue, 36), TruncateString(url, 30))
		}
		err = rows.Err()
		if err != nil {
			log.Fatal(err)
		}
		writer.Flush()
	},
}

func init() {
	rootCmd.AddCommand(listCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// listCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// listCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
