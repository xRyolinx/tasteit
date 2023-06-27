------------------------- People-----------------------------
CREATE TABLE people
(
    id INTEGER NOT NULL PRIMARY KEY,

    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    pdp BLOB NOT NULL,
    admin INTEGER NOT NULL
);

--------------------------- Restaurants---------------------------
CREATE TABLE restaurants
(
    id INTEGER NOT NULL PRIMARY KEY,

    name TEXT NOT NULL,
    type TEXT NOT NULL,

    work_hours INTEGER NOT NULL,
    work_days INTEGER NOT NULL,

    adress TEXT NOT NULL,
    rating INTEGER NOT NULL,
    photo BLOB NOT NULL
);

CREATE TABLE specialities
(
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE restaurant_speciality
(
    id INTEGER NOT NULL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    speciality_id INTEGER NOT NULL,

    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
    FOREIGN KEY (speciality_id) REFERENCES specialities (id)
);

CREATE TABLE comments_restaurant
(
    id INTEGER NOT NULL PRIMARY KEY,

    person_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,

    comment TEXT NOT NULL,
    
    FOREIGN KEY (person_id) REFERENCES people (id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
);


----------------------- DISHES -----------------------

CREATE TABLE dishes
(
    id INTEGER NOT NULL PRIMARY KEY,

    name TEXT NOT NULL,
    type TEXT NOT NULL,
    price INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    photo BLOB NOT NULL
);

CREATE TABLE ingredients
(
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE dish_ingredient
(
    id INTEGER NOT NULL PRIMARY KEY,

    dish_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,

    FOREIGN KEY (dish_id) REFERENCES dishes (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

CREATE TABLE restaurant_dish
(
    id INTEGER NOT NULL PRIMARY KEY,

    restaurant_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,

    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
    FOREIGN KEY (dish_id) REFERENCES dishes (id)
);

CREATE TABLE comments_dish
(
    id INTEGER NOT NULL PRIMARY KEY,

    person_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,

    comment TEXT NOT NULL,
    
    FOREIGN KEY (person_id) REFERENCES people (id),
    FOREIGN KEY (dish_id) REFERENCES dishes (id)
);