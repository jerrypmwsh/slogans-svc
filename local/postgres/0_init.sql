CREATE TABLE IF NOT EXISTS SOURCE(
    id SERIAL PRIMARY KEY, 
    source VARCHAR(100), 
    update_date_time TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS CATEGORY(
    id SERIAL PRIMARY KEY, 
    category VARCHAR(100), 
    update_date_time TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS SLOGAN(
    id SERIAL PRIMARY KEY,
    slogan VARCHAR(200),
    company VARCHAR(100),
    category_id INT REFERENCES category,
    source_id INT REFERENCES source,
    source_info VARCHAR(100),
    update_date_time TIMESTAMPTZ
);
