package main

import (
	"html/template"
	"net/http"
	"time"

	"github.com/dustin/go-humanize"
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

func time_humanize(timestamp uint32) string {
	t := time.Unix(int64(timestamp), 0)
	return humanize.Time(t)
}

func safeHTML(htmlContent string) template.HTML {
	return template.HTML(htmlContent)
}

func main() {
	gin.SetMode(gin.DebugMode)
	router := gin.Default()

	// Template laden
	router.SetFuncMap(template.FuncMap{
		"time_humanize": time_humanize,
		"safe_html":     safeHTML,
	})
	router.LoadHTMLGlob("templates/*")
	router.StaticFS("/static", http.Dir("./static"))

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{})
	})

	hits := []Hit{{"Apfel", "http://apfel.com", 0.98, "Ein <em>Apfel</em> am Tag hält den Arzt fern", 1712670481}, {"Banane", "http://banana.com", 0.98, "Ein <em>Apfel</em> ist nicht so krumm wie eine Banane", 1712670481}}

	router.GET("/q", func(c *gin.Context) {

		var q Query
		c.Bind(&q)

		// HTML-Template rendern und Daten übergeben
		c.HTML(http.StatusOK, "index.html", gin.H{
			"Keyword": q.Keyword,
			"Hits":    hits,
		})
	})

	router.Run() // Standardmäßig auf :8080
}
