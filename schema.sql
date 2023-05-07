DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS access;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS masters;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS shopping_session;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS services;

CREATE TABLE access (
    access_id VARCHAR(32) NOT NULL,
    role INTEGER NOT NULL default 2,
    FOREIGN KEY (access_id) REFERENCES users (user_id),
    PRIMARY KEY(access_id)
);

CREATE TABLE users (
    user_id INTEGER NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    second_name VARCHAR(32) NOT NULL,
    age INT(8) NOT NULL,
    number VARCHAR(15),
    email VARCHAR(32) NOT NULL,
    pswd VARCHAR(32) NOT NULL,
    pic_name_u VARCHAR(32) DEFAULT "unauthorized_user.png",
    PRIMARY KEY(user_id)
);

CREATE TABLE reviews (
    review_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    master_id INTEGER,
    item_id INTEGER,
    rating INTEGER NOT NULL default 2,
    comments  VARCHAR(32) NOT NULL,
    FOREIGN KEY (master_id) REFERENCES users (master_id),
    FOREIGN KEY (item_id) REFERENCES users (item_id),
    FOREIGN KEY (reviewer_id) REFERENCES users (user_id),
    PRIMARY KEY(review_id)
);

CREATE TABLE masters (
    master_id INTEGER NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    second_name VARCHAR(32) NOT NULL,
    patronymic_name VARCHAR(32) NOT NULL,
    experience INT(8) NOT NULL,
    description VARCHAR(15),
    pic_name_m VARCHAR(32) DEFAULT "unauthorized_master.png",
    PRIMARY KEY(master_id)
);



CREATE TABLE items (
    item_id INTEGER NOT NULL,
    item_category INTEGER NOT NULL,
    item_name VARCHAR(32) NOT NULL,
    item_description VARCHAR(32) NOT NULL,
    item_price INTEGER NOT NULL,
    pic_name_i VARCHAR(32) DEFAULT "default_item.png",
    PRIMARY KEY(item_id)
);

CREATE TABLE orders (
    order_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    PRIMARY KEY(order_id)
);

CREATE TABLE shopping_session (
    shop_session_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    PRIMARY KEY(shop_session_id)
);

CREATE TABLE carts (
    cart_item_id INTEGER NOT NULL,
    shop_session_id_FK INTEGER NOT NULL,
    item_id_FK INTEGER NOT NULL,
    FOREIGN KEY (shop_session_id_FK) REFERENCES shopping_session (shop_session_id),
    FOREIGN KEY (item_id_FK) REFERENCES items (item_id)
    PRIMARY KEY(cart_item_id)
);

CREATE TABLE services (
    service_id INTEGER NOT NULL,
    service_name VARCHAR(32) NOT NULL,
    service_price INTEGER NOT NULL,
    pic_name_s VARCHAR(32) DEFAULT "service_and_price1.jpg",
    PRIMARY KEY(service_id)
);
