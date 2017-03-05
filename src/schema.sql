

CREATE TABLE mines (
    mine_id int PRIMARY KEY,
    mine_name varchar(50),
    owners varchar(300),
    development_stage varchar(50),
    activity_status varchar(50),
    lat float,
    lon float
);

CREATE TABLE companies (
  name varchar(50) PRIMARY KEY,
  url varchar(500),
  ticker varchar(10),
  market_cap float
);


CREATE TABLE company_news (
  link text primary key,
  title text,
  ticker varchar(10),
  source varchar(50),
  description text,
  date date
)


CREATE TABLE google_news (
    mine_id int,
    mine_name varchar(50),
    link varchar(500),
    title varchar(500),
    description varchar(1000),
    source varchar(100),
    date date
);


CREATE TABLE google_scholar (
    mine_id int,
    mine_name varchar(50),
    link varchar(500),
    title varchar(500),
    cited_by int,
    author varchar(100)
);


CREATE TABLE claims_geo (
    claim_id int,
    mtrs varchar(100),
    poly_str varchar(1000),
    poly geography(POLYGON,4326)
);

CREATE TABLE claims_meta (
    mtrs varchar(100),
    loc varchar(10),
    claim_type varchar(200),
    claim_count float
);

CREATE TABLE faults (
    name text,
    ftype varchar(100),
    length float,
    sliprate varchar(10),
    slipcode int,
    slipsense varchar(10),
    age varchar(50),
    fault_str text,
    fault geography(LINESTRING, 4326)
);
