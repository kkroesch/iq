#!/bin/sh

# Export all documents from OpenSearch

INDEX="webdocuments"

sroll_id=$(curl -s -X POST "localhost:9200/${INDEX}/_search?scroll=1m" -H "Content-Type: application/json" -d'
{
  "size": 100,
  "query": {
    "match_all": {}
  }
}' | jq -r '._scroll_id')


curl -X POST "localhost:9200/_search/scroll" -H "Content-Type: application/json" -d'
{
  "scroll": "1m",
  "scroll_id": "your_scroll_id"
}'
