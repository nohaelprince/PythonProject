DROP TABLE IF EXISTS mailing CASCADE;
CREATE TABLE mailing(
  addr varchar(255) NOT NULL);

DROP TABLE IF EXISTS domains CASCADE;
CREATE TABLE domains(
  id bigserial primary key, 
  domain_name varchar(20) NOT NULL,
  cnt int, 
  date_of_entry date NOT NULL);
