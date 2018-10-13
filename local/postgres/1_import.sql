-- import tables
copy category(id, category)
from '/docker-entrypoint-initdb.d/tbl_category.csv' DELIMITER ',' CSV;

copy source("id", "source")
from '/docker-entrypoint-initdb.d/tbl_source.csv' DELIMITER ',' CSV; 

copy slogan(id, slogan, company, source_info, category_id, source_id)
from '/docker-entrypoint-initdb.d/tbl_slogans.csv' DELIMITER ',' CSV; 

-- update time
update category
set update_date_time = now();

update source
set update_date_time = now();

update slogan
set update_date_time = now();

-- update autoincrement for tables
select setval(pg_get_serial_sequence('category', 'id'), 
    (select max(id) from category) 
); 
select setval(pg_get_serial_sequence('source', 'id'), 
    (select max(id) from source) 
);
select setval(pg_get_serial_sequence('slogan', 'id'), 
    (select max(id) from slogan) 
);
