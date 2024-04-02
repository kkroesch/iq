# iQ Personal Search Engine

## Installation & Run

```
podman build -f Containerfile -t iqsearch:latest .
podman kube play containers/yaml/iq.yaml
```

### Opensearch


```
curl -X GET "https://localhost:9200/_cat/nodes?v" -ku admin:admin

curl -X PUT "localhost:9200/webdocuments" -H "Content-Type: application/json" -d'
{
  "settings" : {
    "number_of_shards" : 1,
    "number_of_replicas" : 1
  }
}' -ku admin:admin
```

### Solr

```bash
# Start Solr
podman run -d -v "$PWD/solrdata:/var/solr" -p 8983:8983 docker.io/solr:9.4.1-slim
# Fix permissions
chown -R 108982:108982 "$PWD/solrdata"
# Create Core
podman exec  -it my_solr solr create_core -c crawler
```



### FastAPI and Python Dependencies

```
buildah build -f Containerfile -t iqsearch:latest
```

Developemnt server: 

```
uvicorn iq.server:app --reload
```

### Haystack


## Export von URLs

Die URLs können aus der Browser-History, z.B. Brave, Chrome, etc. extrahiert werden:

```
sqlite3 History "SELECT distinct(url) from urls" | awk -F'[?#]' '{split($1, a, "/"); print a[1]"//"a[3]"/"a[4]}' | uniq > history.txt
```
