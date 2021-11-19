WITH staging AS (
    SELECT given_name, family_name, organization, orc_id
    FROM staging.author_{{ ts_nodash  }}_{{ params.subject }}
)

INSERT INTO production.author (given_name, family_name, organization, orc_id) SELECT * FROM staging
ON CONFLICT (given_name, family_name, orc_id) DO NOTHING;