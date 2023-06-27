-- INSERT INTO dishes (name, type, price, rating, photo) VALUES('nom', 'type', 1000, 5, 0);

-- INSERT INTO restaurants (name, type, work_hours, work_days, adress, rating, photo)
-- VALUES('nom1', 'type1', 8, 5, 'boulevard', 4, 0);

-- INSERT INTO restaurant_dish (restaurant_id, dish_id) VALUES(1,1);

-- INSERT INTO ingredients (name) VALUES('Viande');


-- INSERT INTO dish_ingredient (dish_id, ingredient_id) VALUES(11,1);


-- SELECT * FROM ingredients WHERE id IN (SELECT ingredient_id FROM dish_ingredient WHERE dish_id = 14);

INSERT INTO people (username, email, password, admin)
VALUES ('admin', 'admin@taste.com', 'admin123', 1);

-- CREATE TABLE people
-- (
--     id INTEGER NOT NULL PRIMARY KEY,

--     username TEXT NOT NULL,
--     email TEXT NOT NULL,
--     password TEXT NOT NULL,

--     pdp BLOB,
--     admin INTEGER NOT NULL,

--     first_name TEXT,
--     last_name TEXT,
--     adress TEXT,
--     phone TEXT
-- );
