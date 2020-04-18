-- Create Database [movierecommender]
CREATE database IF NOT EXISTS movie_Recommender
DEFAULT CHARACTER SET utf8;
-- DEFAULT COLLATE utf8mb4_0900_ai_ci;

SET default_storage_engine = InnoDB;


-- Specify Database [movierecommender]
USE movie_Recommender;


-- Create Table [movies_metadata]
DROP TABLE IF EXISTS `movie_Recommender`.`movies_metadata`;
CREATE TABLE `movie_Recommender`.`movies_metadata` (
  `id` int NOT NULL,
  `imdb_id` varchar(255),
  `overview` text,
  `popularity` float,
  `poster_path` varchar(255),
  `release_date` varchar(255),
  `tagline` text,
  `title` varchar(255),
  `vote_average` DECIMAL(20, 10),
  `vote_count` int,
  `collection` int,
  PRIMARY KEY (`id`)
); 

--  Import Data from [movies_metadata.csv] to [movies_metadata]
-- load data local infile 'movies_metadata_new.csv' 
load data infile 'movies_metadata_processed.csv' 
INTO TABLE movies_metadata  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [movie_genre]
DROP TABLE IF EXISTS `movie_Recommender`.`movie_genre`;
CREATE TABLE `movie_Recommender`.`movie_genre` (
  `id` int NOT NULL,
  `genre` varchar(30) NOT NULL,
  PRIMARY KEY (`id`, `genre`)
); 


--  Import Data from [movie_genre.csv] to [movie_genre]
-- load data local infile 'movie_genre.csv' 
load data infile 'movies_genre.csv' 
INTO TABLE movie_genre  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Create Table [ratings]
-- DROP TABLE IF EXISTS `movie_Recommender`.`ratings`;
-- CREATE TABLE `movie_Recommender`.`ratings` (
--   `userid` int NOT NULL,
--   `movieid` int NOT NULL,
--   `rating` float NOT NULL,
--   `timestamp` int NOT NULL,
--   PRIMARY KEY (`userid`, `movieid`)
-- ); 

--  Import Data from [ratings.csv] to [ratings]
-- load data local infile 'ratings.csv' 
-- load data infile 'ratings.csv' 
-- INTO TABLE ratings  
-- FIELDS TERMINATED BY ','  
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS;


-- Create Table [ratings_small]
-- DROP TABLE IF EXISTS `movie_Recommender`.`ratings_small`;
-- CREATE TABLE `movie_Recommender`.`ratings_small` (
--   `userid` int NOT NULL,
--   `movieid` int NOT NULL,
--   `rating` float NOT NULL,
--   `timestamp` int NOT NULL,
--   PRIMARY KEY (`userid`, `movieid`)
-- ); 

--  Import Data from [ratings_small.csv] to [ratings_small]
-- load data local infile 'ratings_small.csv' 
-- load data infile 'ratings_small.csv' 
-- INTO TABLE ratings_small  
-- FIELDS TERMINATED BY ','  
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS;


-- Create Table [credits]
-- DROP TABLE IF EXISTS `movie_Recommender`.`credits`;
-- CREATE TABLE `movie_Recommender`.`credits` (
-- 	`cast` text,
--     `crew` text,
--     `id` int NOT NULL,
--     PRIMARY KEY (`id`)
-- );

--  Import Data from [credits.csv] to [credits]
-- load data local infile 'credits.csv'
-- load data infile 'credits.csv' 
-- INTO TABLE credits 
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS;


-- Create Table [keywords]
-- DROP TABLE IF EXISTS `movie_Recommender`.`keywords`;
-- CREATE TABLE `movie_Recommender`.`keywords` (
--     `id` int NOT NULL,
--     `keywords` text,
--     PRIMARY KEY (`id`)
-- );

--  Import Data from [keywords.csv] to [keywords]
-- load data local infile 'keywords.csv' 
-- load data infile 'keywords.csv' 
-- INTO TABLE keywords 
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS;


-- Create Table [links]
-- DROP TABLE IF EXISTS `movie_Recommender`.`links`;
-- CREATE TABLE `movie_Recommender`.`links` (
--     `movieid` int NOT NULL,
--     `imdbid` varchar(25),
--     `tmdbid` varchar(25),
--     PRIMARY KEY (`movieid`)
-- );

--  Import Data from [links.csv] to [links]
-- load data local infile 'links.csv' 
-- load data infile 'links.csv' 
-- INTO TABLE links 
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS;


-- Create Table [links_small]
-- DROP TABLE IF EXISTS `movie_Recommender`.`links_small`;
-- CREATE TABLE `movie_Recommender`.`links_small` (
--     `movieid` int NOT NULL,
--     `imdbid` int NOT NULL,
--     `tmdbid` int NOT NULL,
--     PRIMARY KEY (`movieid`, `imdbid`, `tmdbid`)
-- );

--  Import Data from [links_small.csv] to [links_small]
-- load data local infile 'links_small.csv'
-- load data infile 'links_small.csv' 
-- INTO TABLE links_small 
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS;