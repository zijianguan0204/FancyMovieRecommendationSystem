-- Create Database [movierecommender]
CREATE database IF NOT EXISTS movierecommender
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8mb4_0900_ai_ci;

SET default_storage_engine = InnoDB;


-- Specify Database [movierecommender]
USE movierecommender;


-- Create Table [movies_metadata]
CREATE TABLE `movierecommender`.`movies_metadata` (
  `adult` BOOLEAN NOT NULL,
  `belongs_to_collection` varchar(510),
  `budget` int UNSIGNED NOT NULL,
  `genres` varchar(510) NOT NULL,
  `homepage` varchar(255),
  `id` int NOT NULL,
  `imdb_id` varchar(255) UNIQUE NOT NULL,
  `original_language` varchar(10) NOT NULL,
  `original_title` varchar(255) UNIQUE NOT NULL,
  `overview` varchar(510),
  `popularity` DECIMAL NOT NULL,
  `poster_path` varchar(255) UNIQUE NOT NULL,
  `production_companies` varchar(510) NOT NULL,
  `production_countries` varchar(510) NOT NULL,
  `release_date` DATE NOT NULL,
  `revenue` int NOT NULL,
  `runtime` DECIMAL NOT NULL,
  `spoken_languages` varchar(255) NOT NULL,
  `status` varchar(25) NOT NULL,
  `tagline` varchar(255),
  `title` varchar(255),
  `video` BOOLEAN,
  `vote_average` DECIMAL,
  `vote_count` int,
  PRIMARY KEY (`id`)
); 

--  Import Data from [movies_metadata.csv] to [movies_metadata]
load data local infile 'movies_metadata_new.csv' 
INTO TABLE movies_metadata  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [ratings]
CREATE TABLE `movierecommender`.`ratings` (
  `userid` int NOT NULL,
  `movieid` int NOT NULL,
  `rating` float NOT NULL,
  `timestamp` int NOT NULL,
  PRIMARY KEY (`userid`, `movieid`)
); 

--  Import Data from [ratings.csv] to [ratings]
load data local infile 'ratings.csv' 
INTO TABLE ratings  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [ratings_small]
CREATE TABLE `movierecommender`.`ratings_small` (
  `userid` int NOT NULL,
  `movieid` int NOT NULL,
  `rating` float NOT NULL,
  `timestamp` int NOT NULL,
  PRIMARY KEY (`userid`, `movieid`)
); 

--  Import Data from [ratings_small.csv] to [ratings_small]
load data local infile 'ratings_small.csv' 
INTO TABLE ratings_small  
FIELDS TERMINATED BY ','  
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [credits]
CREATE TABLE `movierecommender`.`credits` (
	`cast` text,
    `crew` text,
    `id` int NOT NULL,
    PRIMARY KEY (`id`)
);

--  Import Data from [credits.csv] to [credits]
load data local infile 'credits.csv' 
INTO TABLE credits 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [keywords]
CREATE TABLE `movierecommender`.`keywords` (
    `id` int NOT NULL,
    `keywords` text,
    PRIMARY KEY (`id`)
);

--  Import Data from [keywords.csv] to [keywords]
load data local infile 'keywords.csv' 
INTO TABLE keywords 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [links]
CREATE TABLE `movierecommender`.`links` (
    `movieid` int NOT NULL,
    `imdbid` varchar(25),
    `tmdbid` varchar(25),
    PRIMARY KEY (`movieid`)
);

--  Import Data from [links.csv] to [links]
load data local infile 'links.csv' 
INTO TABLE links 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


-- Create Table [links_small]
CREATE TABLE `movierecommender`.`links_small` (
    `movieid` int NOT NULL,
    `imdbid` int NOT NULL,
    `tmdbid` int NOT NULL,
    PRIMARY KEY (`movieid`, `imdbid`, `tmdbid`)
);

--  Import Data from [links_small.csv] to [links_small]
load data local infile 'links_small.csv' 
INTO TABLE links_small 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;