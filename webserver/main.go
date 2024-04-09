package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Query struct {
	Keyword string `form:"query"`
}

func main() {
	gin.SetMode(gin.DebugMode)
	router := gin.Default()

	// Template laden
	router.LoadHTMLGlob("templates/*")
	router.StaticFS("/static", http.Dir("./static"))

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{})
	})

	router.GET("/q", func(c *gin.Context) {
		hits := []string{"Apfel", "Banane", "Kirsche"}
		var q Query
		c.Bind(&q)
		fmt.Print("Search for", q.Keyword)

		// HTML-Template rendern und Daten übergeben
		c.HTML(http.StatusOK, "index.html", gin.H{
			"Keyword": q.Keyword,
			"Hits":    hits,
		})
	})

	router.Run() // Standardmäßig auf :8080
}
