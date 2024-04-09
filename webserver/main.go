package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Query struct {
	Keyword string `form:"query"`
}

type Hit struct {
	Title   string
	Url     string
	Score   float32
	Hilite  string
	Indexed uint32
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
		hits := []Hit{{"Apfel", "http://apfel.com", 0.98, "Ein <em>Apfel</em> am Tag hält den Arzt fern", 1712670481}, {"Banane", "http://banana.com", 0.98, "Ein <em>Apfel</em> ist nicht so krumm wie eine Banane", 1712670481}}

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
