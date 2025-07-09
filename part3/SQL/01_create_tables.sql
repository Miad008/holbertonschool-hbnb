-- 01_create_tables.sql

-- Create User table
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    email      VARCHAR(120) NOT NULL UNIQUE,
    password   VARCHAR(128) NOT NULL,
    is_admin   BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Place table
CREATE TABLE IF NOT EXISTS places (
    id          CHAR(36) PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    price       DECIMAL(10,2) NOT NULL,
    latitude    FLOAT        NOT NULL,
    longitude   FLOAT        NOT NULL,
    owner_id    CHAR(36)     NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Amenity table
CREATE TABLE IF NOT EXISTS amenities (
    id          CHAR(36) PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Review table
CREATE TABLE IF NOT EXISTS reviews (
    id          CHAR(36) PRIMARY KEY,
    text        TEXT        NOT NULL,
    rating      INT         NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id     CHAR(36)    NOT NULL,
    place_id    CHAR(36)    NOT NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id)   ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id)  ON DELETE CASCADE,
    UNIQUE (user_id, place_id)  -- one review per user/place
);

-- Association table for Place ↔ Amenity (many-to-many)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id   CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id)   ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

