CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    birth_year INT NOT NULL,
    home_lat NUMERIC(7, 6) NOT NULL,
    home_lon NUMERIC(7, 6) NOT NULL,
    gender TEXT NOT NULL,
    is_admin BOOLEAN
);

CREATE TABLE boards(
    board_id SERIAL PRIMARY KEY,
    header TEXT NOT NULL,
    is_city BOOLEAN,
    pos_lat NUMERIC(7, 6),
    pos_lon NUMERIC(7, 6)
);

CREATE TABLE admin_privs(
    admin_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    board_id INT NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (board_id)
        REFERENCES boards (board_id)
        ON DELETE CASCADE
);

CREATE TABLE posts(
    post_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    owner_id INT NOT NULL,
    header TEXT NOT NULL,
    content TEXT,
    pos_lat NUMERIC(7, 6),
    pos_lon NUMERIC(7, 6),
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE
);

CREATE TABLE up_votes(
    vote_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (post_id)
        REFERENCES posts (post_id)
        ON DELETE CASCADE

);

CREATE TABLE comments(
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    timestamp TIMESTAMP,
    owner_id INT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (owner_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (post_id)
        REFERENCES posts (post_id)
        ON DELETE CASCADE
);