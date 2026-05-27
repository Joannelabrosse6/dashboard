CREATE DATABASE IF NOT EXISTS vod_analysis;
USE vod_analysis;

-- Table 1: movies
-- Contient les informations de base des séries/films
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,  -- Contrainte UNIQUE et NOT NULL
    release_year INT NOT NULL,           -- Contrainte NOT NULL
    platform VARCHAR(100),
    internal_score DECIMAL(5,2),
    global_rating DECIMAL(5,2)           -- Sera rempli par l'API
);

-- Table 2: genres
-- Contient les différents genres
CREATE TABLE IF NOT EXISTS genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE    -- Contrainte UNIQUE
);

-- Table 3: movie_genres (Table de jointure pour relation many-to-many)
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    -- Contraintes FOREIGN KEY
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

-- Création d'une Vue
-- Cette vue permet de récupérer rapidement les films ayant été évalués par l'API
CREATE OR REPLACE VIEW vw_movie_performance AS
SELECT m.title, m.platform, m.internal_score, m.global_rating
FROM movies m
WHERE m.global_rating IS NOT NULL;

-- Création d'une Fonction Stockée
-- Cette fonction catégorise un film selon son score
DELIMITER //
DROP FUNCTION IF EXISTS get_movie_status //
CREATE FUNCTION get_movie_status(score DECIMAL(5,2)) RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    IF score >= 90.0 THEN
        RETURN 'Excellent';
    ELSEIF score >= 80.0 THEN
        RETURN 'Good';
    ELSE
        RETURN 'Average';
    END IF;
END //
DELIMITER ;

-- Insertion de quelques données de base pour les genres (le reste sera fait en Python)
INSERT INTO genres (name) VALUES 
('Drama'), 
('Comedy'), 
('Action'), 
('Sci-Fi'), 
('Thriller'),
('Crime')
ON DUPLICATE KEY UPDATE name=name;
