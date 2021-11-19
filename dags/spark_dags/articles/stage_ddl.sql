CREATE TABLE IF NOT EXISTS staging.publisher_{{ ts_nodash  }}_{{ params.subject }} (
    publisher_id SERIAL PRIMARY KEY,
    publisher_name VARCHAR NOT NULL    
);

CREATE TABLE IF NOT EXISTS staging.journal_{{ ts_nodash  }}_{{ params.subject }} (
    journal_id SERIAL PRIMARY KEY,
    journal_name VARCHAR NOT NULL    
);

CREATE TABLE IF NOT EXISTS staging.author_{{ ts_nodash  }}_{{ params.subject }} (
    author_id SERIAL PRIMARY KEY,
    given_name VARCHAR NOT NULL,
    family_name VARCHAR NOT NULL,
    organization VARCHAR,
    orc_id VARCHAR    
);

CREATE TABLE IF NOT EXISTS staging.articles_{{ ts_nodash  }}_{{ params.subject }} (
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