-- make sure user exists
DO
$body$
BEGIN
  IF NOT EXISTS (
    SELECT
      *
    FROM
      pg_catalog.pg_user
    WHERE
      usename = 'caitlinjobs'
  ) THEN
    CREATE ROLE caitlinjobs LOGIN PASSWORD 'caitlinjobs';
  END IF;
END
$body$
;


-- create the database
CREATE DATABASE caitlinjobs OWNER caitlinjobs;
