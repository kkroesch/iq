package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	gin.SetMode(gin.DebugMode)
	router := gin.Default()

	// Template laden
	router.LoadHTMLGlob("templates/*")
	router.StaticFS("/static", http.Dir("./static"))

	router.GET("/", func(c *gin.Context) {
		hits := []string{"Apfel", "Banane", "Kirsche"}
		// HTML-Template rendern und Daten übergeben
		c.HTML(http.StatusOK, "index.html", gin.H{
			"Hits": hits,
		})
	})

	router.Run() // Standardmäßig auf :8080
}
