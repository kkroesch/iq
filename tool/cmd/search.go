/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"fmt"
	"io"
	"net/http"
	"net/url"

	"github.com/spf13/cobra"
)

var (
	query string
)

//var solrUrl = os.Getenv("SOLR_URL")
//client := solr.NewJSONClient(solrUrl)

// searchCmd represents the search command
var searchCmd = &cobra.Command{
	Use:   "search",
	Short: "Search for keywords.",
	Long:  `Search for keyword and return relevant document chunks`,
	Run: func(cmd *cobra.Command, args []string) {
		baseURL := "http://localhost:8983/solr/websites/select"
		params := url.Values{}
		params.Add("fl", "id,title,last_seen,url,score")
		params.Add("hl.fl", "body")
		params.Add("hl", "true")
		params.Add("indent", "true")
		params.Add("q.op", "OR")
		params.Add("q", fmt.Sprintf("body:%s", query))

		response, err := http.Get(fmt.Sprintf("%s?%s", baseURL, params.Encode()))
		if err != nil {
			panic(err)
		}
		defer response.Body.Close()

		body, err := io.ReadAll(response.Body)
		if err != nil {
			panic(err)
		}

		fmt.Println(string(body))
	},
}

func init() {
	rootCmd.AddCommand(searchCmd)
	searchCmd.PersistentFlags().StringVarP(&query, "query", "q", "", "Keyword")
}
