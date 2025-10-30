CREATE DATABASE IF NOT EXISTS bike_rental CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bike_rental;
CREATE TABLE stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(200) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE bicycles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    status ENUM('available', 'in_repair', 'removed') NOT NULL,
    station_id INT,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role ENUM('manager', 'client') NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bicycle_id INT,
    user_id INT,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    cost DECIMAL(10,2),
    FOREIGN KEY (bicycle_id) REFERENCES bicycles(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE INDEX idx_rental_start_time ON rentals(start_time);
INSERT INTO stations (address) VALUES 
('вул. Центральна, 10'),
('вул. Паркова, 5');
INSERT INTO bicycles (model, status, station_id) VALUES 
('Trek 820', 'available', 1),
('Giant Escape', 'available', 2),
('Specialized Rockrider', 'in_repair', 1);
INSERT INTO users (role, username, password) VALUES 
('manager', 'manager1', '$2b$12$hUsNDQNJoTCReXx2Yo40M.G0kd2.XV9hwiaSh.c5CAT5QJy77IomK'),
('client', 'client1', '$2b$12$ul7NFSz.UE4qCmrfW30ciOm18uqzTsYkn.9KpeI2NJYC25efO.V2q');