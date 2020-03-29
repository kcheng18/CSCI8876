CREATE TABLE keywords (
    kid int NOT NULL AUTO_INCREMENT,
    keyword CHAR(50) NOT NULL,
    PRIMARY KEY (kid));

CREATE TABLE authors (
    aid int NOT NULL AUTO_INCREMENT,
    name CHAR(50) NOT NULL,
    PRIMARY KEY (aid));

create table literatures(
    pmid int NOT NULL,
    title CHAR(250) NOT NULL,
    abstract TEXT NOT NULL,
    date date not null,
    PRIMARY KEY (pmid));

create table search(
    pmid int NOT NULL,
    kid int NOT NULL,
    PRIMARY KEY (pmid, kid),
    FOREIGN KEY (kid) REFERENCES keywords(kid),
    FOREIGN KEY (pmid) REFERENCES literatures(pmid));

create table written(
    pmid int NOT NULL,
    aid int NOT NULL,
    PRIMARY KEY (pmid, aid),
    FOREIGN KEY (aid) REFERENCES authors(aid),
    FOREIGN KEY (pmid) REFERENCES literatures(pmid));