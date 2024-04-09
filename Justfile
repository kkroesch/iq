build_tool:
    #!/bin/bash
    cd tool
    go build -o build

build_container:
    podman build -t iq:lastest -f Containerfile .

build:
    just build_tool
    just build_container

solr:
    [[ $(podman volume ls | grep solr_data) ]] || podman volume create solr_data
    podman run -d -v "solr_data:/var/solr" -p 8983:8983 --name local_solr docker.io/solr:9.5
    sleep 20
    podman exec -it local_solr solr create_core -c websites

