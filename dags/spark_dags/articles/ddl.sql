CREATE TABLE IF NOT EXISTS production.publisher (
    publisher_id SERIAL PRIMARY KEY,
    publisher_name VARCHAR NOT NULL    
);

CREATE TABLE IF NOT EXISTS production.journal (
    journal_id SERIAL PRIMARY KEY,
    journal_name VARCHAR NOT NULL    
);

CREATE TABLE IF NOT EXISTS production.author (
    author_id SERIAL PRIMARY KEY,
    given_name VARCHAR NOT NULL,
    family_name VARCHAR NOT NULL,
    organization VARCHAR,
    orc_id VARCHAR,
    UNIQUE(given_name, family_name, orc_id)    
);

CREATE TABLE IF NOT EXISTS production.articles (
    article_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    doi VARCHAR NOT NULL,
    uri VARCHAR,
    publisher_id INTEGER REFERENCES publisher (publisher_id),
    journal_id INTEGER REFERENCES journal (journal_id),
    print_issn VARCHAR,
    electronic_issn VARCHAR,
    date_created DATE,
    date_deposited DATE,
    date_indexed DATE
);