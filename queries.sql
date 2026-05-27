USE vod_analysis;

-- 1. Requête simple avec WHERE et ORDER BY
-- Sélectionne les séries récentes (depuis 2018) triées par score interne décroissant
SELECT title, release_year, platform, internal_score 
FROM movies 
WHERE release_year >= 2018 
ORDER BY internal_score DESC;

-- 2. Requête avec LIMIT pour les Top 3
-- Récupère le Top 3 des séries selon l'API externe (rating global)
SELECT title, global_rating 
FROM movies 
ORDER BY global_rating DESC 
LIMIT 3;

-- 3. Requête avec GROUP BY, HAVING, ORDER BY
-- Calcule le nombre de séries et le score moyen par plateforme,
-- en ne gardant que les plateformes ayant plus de 1 série
SELECT platform, COUNT(*) as total_movies, AVG(internal_score) as avg_score
FROM movies
GROUP BY platform
HAVING total_movies > 1
ORDER BY avg_score DESC;

-- 4. Requête avec Jointure sur 3 tables (movies, movie_genres, genres)
-- Récupère le titre, la plateforme et le nom du genre pour toutes les séries de genre 'Drama'
SELECT m.title, m.platform, g.name as genre_name
FROM movies m
JOIN movie_genres mg ON m.id = mg.movie_id
JOIN genres g ON mg.genre_id = g.id
WHERE g.name = 'Drama';

-- 5. Requête utilisant un CTE (Common Table Expression)
-- Identifie d'abord les séries dites "Premium" (score interne > 90),
-- puis affiche leurs genres et trie par année de sortie
WITH PremiumSeries AS (
    SELECT id, title, release_year, internal_score
    FROM movies
    WHERE internal_score > 90
)
SELECT p.title, p.release_year, g.name as genre_name, p.internal_score
FROM PremiumSeries p
JOIN movie_genres mg ON p.id = mg.movie_id
JOIN genres g ON mg.genre_id = g.id
ORDER BY p.release_year DESC;
