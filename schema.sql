DROP TABLE IF EXISTS user;

CREATE TABLE access (
    access_id INTEGER NOT NULL,
    role INTEGER NOT NULL default 2,
    PRIMARY KEY(access_id)
);

CREATE TABLE user (
    user_id INTEGER NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    second_name VARCHAR(32) NOT NULL,
    age INT(8) NOT NULL,
    email VARCHAR(32) NOT NULL,
    pswd VARCHAR(32) NOT NULL,
    access_id_FK INTEGER NOT NULL,
    PRIMARY KEY(user_id),
    FOREIGN KEY (access_id_FK) REFERENCES access (access_id)
);