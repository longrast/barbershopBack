DROP TABLE IF EXISTS user;

CREATE TABLE user (
    user_id INTEGER,
    first_name VARCHAR(32) NOT NULL,
    second_name VARCHAR(32) NOT NULL,
    age INT(8) NOT NULL,
    email VARCHAR(32) NOT NULL,
    pswd VARCHAR(32) NOT NULL,
    access_lvl VARCHAR(32) NOT NULL default 2,
    PRIMARY KEY(user_id)
);