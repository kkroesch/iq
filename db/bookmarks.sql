
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER PRIMARY KEY,
    title TEXT NULL,
    url TEXT NOT NULL,
    search_id TEXT NULL,
    last_visited INTEGER NULL,
    status_code INTEGER NULL,
    last_indexed INTEGER NULL
);
CREATE UNIQUE INDEX unique_url ON websites(url);
INSERT INTO websites (url) VALUES ('https://www.redhat.com/sysadmin/quadlet-podman');

INSERT INTO websites 
    (title, url, last_visited, last_indexed, search_id)
    VALUES
    (?, ?, ?, ?, ?)
    ON CONFLICT (url)
    DO UPDATE SET last_visited = strftime('%s', 'now');
