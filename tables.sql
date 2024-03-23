CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    birth_year INT NOT NULL,
    home_lat NUMERIC(7, 6) NOT NULL,
    home_lon NUMERIC(7, 6) NOT NULL,
    gender TEXT NOT NULL,
    is_admin BOOLEAN
);

CREATE TABLE boards (
    board_id SERIAL PRIMARY KEY,
    header TEXT NOT NULL,
    pos_lat NUMERIC(10, 8),
    pos_lon NUMERIC(11, 8)
);

CREATE TABLE admin_privs (
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

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    owner_id INT NOT NULL,
    board_id INT,
    header TEXT NOT NULL,
    content TEXT,
    pos_lat NUMERIC(10, 8),
    pos_lon NUMERIC(11, 8),
    city TEXT,
    suburb TEXT,
    FOREIGN KEY (owner_id)
    REFERENCES users (user_id)
    ON DELETE CASCADE,
    FOREIGN KEY (board_id)
    REFERENCES boards (board_id)
    ON DELETE CASCADE
);

CREATE TABLE votes (
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

CREATE TABLE comments (
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

INSERT INTO users (username, password, birth_year, home_lat , home_lon, gender, is_admin) VALUES ('admin', 'scrypt:32768:8:1$o7GNEB1J3DHw1NMd$25dd6510883c7325f2471193d6137da2d6ee0beb6125e10e4dd307ca2d7c6583428ccb5a18dd1a1897c64e16198c763fb5b7aaab625ac837d1601860cf2e1266', 1990, 0, 0, '?', TRUE);