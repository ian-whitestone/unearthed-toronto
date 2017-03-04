

CREATE TABLE mines (
    mine_id int PRIMARY KEY,
    mine_name varchar(50),
    owners varchar(300),
    development_stage varchar(50),
    activity_status varchar(50),
    lat float,
    lon float
);




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
