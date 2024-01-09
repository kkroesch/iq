# iQ Personal Search Engine

## Installation

### Opensearch

Run OpenSearch with Podman, check and create index:

```
podman run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" --name opensearch-node -d -e "ES_JAVA_OPTS=-Xms1024m -Xmx1024m" docker.io/opensearchproject/opensearch

curl -X GET "https://localhost:9200/_cat/nodes?v" -ku admin:admin

curl -X PUT "localhost:9200/webdocuments" -H "Content-Type: application/json" -d'
{
  "settings" : {
    "number_of_shards" : 1,
    "number_of_replicas" : 1
  }
}' -ku admin:admin
```

Or, copy the `*.container` files in `~/.config/containers/systemd`:

```
systemctl --user daemon-reload
systemctl --user start opensearch.service
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
