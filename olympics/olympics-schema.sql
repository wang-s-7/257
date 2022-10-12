CREATE TABLE athletes (
        id INTEGER,
        name TEXT
    );

CREATE TABLE events (
        id INTEGER,
        name TEXT
    );

CREATE TABLE games (
    id INTEGER,
    year INTEGER,
    season TEXT,
    city TEXT
)

CREATE TABLE nocs (
    id INTEGER,
    abbreviation TEXT,
    name TEXT
)

CREATE TABLE event_results (
    athlete_id INTEGER,
    event_id INTEGER,
    noc_id INTEGER,
    game_id INTEGER,
    medal TEXT
)