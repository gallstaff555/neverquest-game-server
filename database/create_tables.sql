PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users(
   id INTEGER PRIMARY KEY,
   user_name TEXT NOT NULL,
   email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS characters(
    id INTEGER PRIMARY KEY, 
    character TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);