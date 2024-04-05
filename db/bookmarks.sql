-- Sequenz erstellen
CREATE SEQUENCE websites_id_seq;

-- Tabelle erstellen mit expliziter Sequenz für die ID
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER PRIMARY KEY DEFAULT nextval('websites_id_seq'),
    title TEXT NULL,
    url TEXT NOT NULL,
    search_id TEXT NULL,
    category TEXT NULL,
    last_visited INTEGER NULL,
    status_code INTEGER NULL,
    last_indexed INTEGER NULL
);

-- Einzigartigkeit der URL sicherstellen
CREATE UNIQUE INDEX IF NOT EXISTS unique_url ON websites(url);

-- Applikationsnutzer (Lese-/Schreibzugriff)
CREATE ROLE websites_app WITH LOGIN PASSWORD '{{app_password}}';
-- Administrationsnutzer (Lese-/Schreibzugriff, kann erstellen)
CREATE ROLE websites_admin WITH LOGIN PASSWORD '{{admin_password}}' CREATEDB;
-- Reportingnutzer (Nur Leserechte)
CREATE ROLE websites_reporter WITH LOGIN PASSWORD '{{reporter_password}}';

-- Rechte für Applikationsnutzer
GRANT USAGE ON SEQUENCE websites_id_seq TO websites_app;
GRANT SELECT, INSERT, UPDATE ON websites TO websites_app;

-- Rechte für Administrationsnutzer
GRANT USAGE, SELECT, UPDATE ON SEQUENCE websites_id_seq TO websites_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO websites_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO websites_admin;

-- Rechte für Reportingnutzer
GRANT SELECT ON websites TO websites_reporter;

INSERT INTO websites (title, url)
VALUES ($1, $2)
ON CONFLICT (url)
DO UPDATE SET last_visited = EXTRACT(EPOCH FROM NOW());

