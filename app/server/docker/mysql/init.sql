CREATE TABLE IF NOT EXISTS app_settings (
    id INT PRIMARY KEY,
    config_value VARCHAR(255) NOT NULL
);

INSERT INTO app_settings (id, config_value) 
VALUES (1, 'Default Status') 
ON DUPLICATE KEY UPDATE config_value=config_value;

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    image_path VARCHAR(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS halls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rows_count INT NOT NULL,
    seats_per_row INT NOT NULL,
    description TEXT
);


CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    hall_id INT,
    session_date DATETIME NOT NULL,
    seats_map JSON, 
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (hall_id) REFERENCES halls(id) ON DELETE CASCADE
);


SET NAMES 'utf8mb4';
INSERT INTO movies (title, release_year, image_path) VALUES 
('Аватар: Путь воды', 2025, 'movies/avatar2.jpg'),
('Интерстеллар', 2014, 'posters/interstellar.png'),
('Дюна: Часть вторая', 2024, 'images/dune2.webp');

INSERT INTO halls (rows_count, seats_per_row, description) VALUES 
(10, 12, 'Большой зал'),
(5, 6, 'VIP-зал'),
(12, 16, 'IMAX зал');

INSERT INTO sessions (movie_id, hall_id, session_date, seats_map) VALUES 
(1, 2, '2026-02-20 18:30:00', 
 '[
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0]
 ]'),

-- Сеанс в Большом зале
(2, 1, '2026-02-20 21:00:00', 
 '[
  [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
 ]');