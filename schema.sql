DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS access;

CREATE TABLE access (
    access_id VARCHAR(32) NOT NULL,
    role INTEGER NOT NULL default 2,
    FOREIGN KEY (access_id) REFERENCES user (user_id),
    PRIMARY KEY(access_id)
);

CREATE TABLE user (
    user_id INTEGER NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    second_name VARCHAR(32) NOT NULL,
    age INT(8) NOT NULL,
    number VARCHAR(15),
    email VARCHAR(32) NOT NULL,
    pswd VARCHAR(32) NOT NULL,
    PRIMARY KEY(user_id)
);