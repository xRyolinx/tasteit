CREATE TABLE people
(
    id SERIAL NOT NULL PRIMARY KEY,

    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,

    photo BYTEA,
    admin INTEGER NOT NULL,

    first_name TEXT,
    last_name TEXT,
    adress TEXT,
    phone TEXT
);
CREATE TABLE restaurants
(
    id SERIAL NOT NULL PRIMARY KEY,
    person_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    type TEXT NOT NULL,

    work_hours INTEGER NOT NULL,
    work_days INTEGER NOT NULL,

    adress TEXT NOT NULL,
    rating INTEGER NOT NULL,
    photo BYTEA,

    FOREIGN KEY (person_id) REFERENCES people (id)
);
CREATE TABLE specialities
(
    id SERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE restaurant_speciality
(
    id SERIAL NOT NULL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    speciality_id INTEGER NOT NULL,

    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
    FOREIGN KEY (speciality_id) REFERENCES specialities (id)
);
CREATE TABLE dishes
(
    id SERIAL NOT NULL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    type TEXT NOT NULL,
    price INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    photo BYTEA,

    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
);
CREATE TABLE ingredients
(
    id SERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE dish_ingredient
(
    id SERIAL NOT NULL PRIMARY KEY,

    dish_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,

    FOREIGN KEY (dish_id) REFERENCES dishes (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);
CREATE TABLE comments_restaurant
(
    id SERIAL NOT NULL PRIMARY KEY,

    person_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,

    comment TEXT NOT NULL,

    FOREIGN KEY (person_id) REFERENCES people (id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
);
CREATE TABLE comments_dish
(
    id SERIAL NOT NULL PRIMARY KEY,

    person_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,

    comment TEXT NOT NULL,

    FOREIGN KEY (person_id) REFERENCES people (id),
    FOREIGN KEY (dish_id) REFERENCES dishes (id)
);
CREATE TABLE messages
(
    id SERIAL NOT NULL PRIMARY KEY,

    id_sent INTEGER NOT NULL,
    id_received INTEGER NOT NULL,

    message TEXT NOT NULL,

    FOREIGN KEY (id_sent) REFERENCES people (id),
    FOREIGN KEY (id_received) REFERENCES people (id)
);
CREATE TABLE receive
(
    id SERIAL NOT NULL PRIMARY KEY,

    id_user INTEGER NOT NULL,
    id_dest INTEGER NOT NULL,
    val TEXT NOT NULL,


    FOREIGN KEY (id_user) REFERENCES people (id),
    FOREIGN KEY (id_dest) REFERENCES people (id)
);
CREATE INDEX user_index ON receive (id_user);
CREATE INDEX dest_index ON receive (id_dest);
CREATE INDEX sent_index ON messages (id_sent);
CREATE INDEX received_index ON messages (id_received);