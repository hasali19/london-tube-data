CREATE TABLE stations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    latitude DOUBLE PRECISION NOT NULL
);

CREATE TABLE lines (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE stations_lines (
    station_id TEXT NOT NULL REFERENCES stations (id),
    line_id INTEGER NOT NULL REFERENCES lines (id),
    PRIMARY KEY (station_id, line_id)
);
