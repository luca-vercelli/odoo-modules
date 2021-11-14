drop view if exists dbmanager_columns;
drop view if exists dbmanager_tables;
drop view if exists dbmanager_views;
drop function if exists hash(text) ;

create function hash(text) returns int as $$
 select ('x'||substr(md5($1),1,8))::bit(32)::int
$$ language sql;


create view dbmanager_tables as
select hash(table_name) as id,*
from information_schema.tables
where table_schema='public';

create view dbmanager_views as
select hash(table_name) as id,*
from information_schema.views
where table_schema='public';

create view dbmanager_columns as
select hash(table_name||column_name) as id, hash(table_name) as table_id, C.*
from information_schema.columns C
where C.table_schema='public';




