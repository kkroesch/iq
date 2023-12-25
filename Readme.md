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

### FastAPI and Python Dependencies

```
buildah build -f Containerfile -t iqsearch:latest
```


### Haystack
