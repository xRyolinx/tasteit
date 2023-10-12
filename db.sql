CREATE TABLE people
(
    id SERIAL PRIMARY KEY,

    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,

    admin INTEGER NOT NULL,

    first_name TEXT,
    last_name TEXT,
    adress TEXT,
    phone TEXT,
    photo BYTEA
);

CREATE TABLE restaurants
(
    id SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    type TEXT NOT NULL,
    adress TEXT NOT NULL,

    work_hours TEXT,
    work_days TEXT,

    rating INTEGER NOT NULL,

    photo BYTEA,

    FOREIGN KEY (person_id) REFERENCES people (id)
);

CREATE TABLE dishes
(
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    type TEXT NOT NULL,

    price INTEGER NOT NULL,
    rating INTEGER NOT NULL,

    photo BYTEA,

    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
);

CREATE TABLE messages
(
    id SERIAL PRIMARY KEY,

    id_sent INTEGER NOT NULL,
    id_received INTEGER NOT NULL,

    message TEXT NOT NULL,

    FOREIGN KEY (id_sent) REFERENCES people (id),
    FOREIGN KEY (id_received) REFERENCES people (id)
);