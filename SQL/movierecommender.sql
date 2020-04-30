-- Create Database [movierecommender]
CREATE database IF NOT EXISTS movie_Recommender
DEFAULT CHARACTER SET utf8;
-- DEFAULT COLLATE utf8mb4_0900_ai_ci;

SET default_storage_engine = InnoDB;


-- Specify Database [movierecommender]
USE movie_Recommender;


-- Create Table [movies_metadata]
DROP TABLE IF EXISTS `movie_recommender`.`movies_metadata`;
CREATE TABLE `movie_recommender`.`movies_metadata` (
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
DROP TABLE IF EXISTS `movie_recommender`.`movie_genre`;
CREATE TABLE `movie_recommender`.`movie_genre` (
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
DROP TABLE IF EXISTS `movie_recommender`.`ratings`;
CREATE TABLE `movie_recommender`.`ratings` (
  `userid` int NOT NULL,
  `movieid` int NOT NULL,
  `rating` varchar(255),
  `timestamp` varchar(255),
  PRIMARY KEY (`userid`, `movieid`)
); 

--  Import Data from [ratings.csv] to [ratings]
-- load data local infile 'ratings.csv' 
load data infile 'rating_processed.csv' 
INTO TABLE ratings  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Create Table [cast_info]
DROP TABLE IF EXISTS `movie_recommender`.`cast_infor`;
CREATE TABLE `movie_recommender`.`cast_infor` (
	`id` int,
    `name` varchar(255),
    PRIMARY KEY (`id`)
);

--  Import Data from [credits.csv] to [credits]
-- load data local infile 'cast_info.csv'
load data infile 'cast_info.csv' 
INTO TABLE cast_infor
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [crew_info]
DROP TABLE IF EXISTS `movie_recommender`.`crew_info`;
CREATE TABLE `movie_recommender`.`crew_info` (
    `id` int NOT NULL,
    `name` varchar(255),
    PRIMARY KEY (`id`)
);

--  Import Data from [crew_info.csv] to [crew_info]
-- load data local infile 'crew_info.csv' 
load data infile 'crew_info.csv' 
INTO TABLE crew_info 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Create Table [movie_cast]
DROP TABLE IF EXISTS `movie_recommender`.`movie_cast`;
CREATE TABLE `movie_recommender`.`movie_cast` (
    `cast_id` int NOT NULL,
    `movie_id` varchar(255),
    PRIMARY KEY (`cast_id`, `movie_id`)
);

--  Import Data from [movie_cast.csv] to [movie_cast]
-- load data local infile 'movie_cast.csv' 
load data infile 'movie_cast.csv' 
INTO TABLE movie_cast 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Create Table [movie_cast]
DROP TABLE IF EXISTS `movie_recommender`.`movie_crew`;
CREATE TABLE `movie_recommender`.`movie_crew` (
    `crew_id` int NOT NULL,
    `movie_id` varchar(255),
    `job` varchar(255),
    PRIMARY KEY (`movie_id`, `crew_id`, `job`)
);

--  Import Data from [movie_crew.csv] to [movie_crew]
-- load data local infile 'movie_crew.csv' 
load data infile 'movie_crew.csv' 
INTO TABLE movie_crew 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Create Table [recommend_list]
DROP TABLE IF EXISTS `movie_recommender`.`recommend_list`;
CREATE TABLE `movie_recommender`.`recommend_list` (
    `userid` int NOT NULL,
    `movie_list` varchar(255),
    PRIMARY KEY (`userid`)
);