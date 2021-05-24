# Data Modeling Project with PostgreSQL


## 1. Intro of Project
This is the first project of "Data Engineering Nanodegree Program".

### 1.1 Background
Company SM is a startup company, they have a music streaming APP, 
and this APP records users activities in a log file, for better understand their customer behavior and grow their business, 
they would like to analyze these log files and gain more insights from it.

For this purpose, SM need to build a relation dabase for analytics.

Data Engineer's job is to:
* create a PostgreSQL database with star schema
* build a ETL using python to bring data from JSON file into database 

### 1.2 Original Data
Two data scources:
1. Song metadata
Song dataset a from 'Million Song Dataset', here is the link: [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/).
Each file is a JSON format data about one song, below is a example:

		{
		"num_songs": 1, 
		"artist_id": "ARJIE2Y1187B994AB7", 
		"artist_latitude": null, 
		"artist_longitude": null, 
		"artist_location": "", 
		"artist_name": "Line Renaud", 
		"song_id": "SOUPIRU12A6D4FA1E1", 
		"title": "Der Kleine Dompfaff", 
		"duration": 152.92036,
		 "year": 0
		}

2. Music APP log file
These log files contains 
* users activitiy information: who from where at what time click which song on which page using which software
* music information: song name, artist, length


	Below is a example of log JSON file


		{
		"artist": "Survivor",
		"auth": "Logged In",
		"firstName": "Jayden",
		"gender": "M",
		"itemInSession": 0,
		"lastName": "Fox",
		"length": 245.36771,
		"level": "free",
		"location": "New Orleans-Metairie, LA",
		"method": "PUT",
		"page": "NextSong",
		"registration": 1541033612796.0,
		"sessionId": 100,
		"song": "Eye Of The Tiger",
		"status": 200,
		"ts": 1541110994796,
		"userAgent": "\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
		"userId": "101"
		}

## 2. Create Database
### 2.1 Schema

Below is the schema,
One fact table: *Songplays*

4 dimension tables: *Users, Time, Song, Artist*

	**********                     ***********          *************
    *  User  * <---         --->   *  Song  *   --->    *  Artist  *   
	**********      |       |      ***********          *************	
			|	|
			|	|
			***************	
			*  songplays  *  
			***************
			|
			|
	**********	|
  	*  Time  * <---
	**********		

## 2.2 Database
Use **create_tables.py** to create database *sparkifydb*, based on the aboved schema.

You can use **test.ipynb** to test whether you successfully create the database.

## 3. ETL

ETL in this project use python scripts to process & bring data from song file and log file into *sparkifydb*.

Use python function *os.walk, os.path, glob.glob* to walk through folders which contain source JSON file, 
for each JSON files, use Pandas dataframe to filter, slice and then write it to destination table in *sparkifydb*.

### 3.1 Song JSON
use python dataframe, and slicing dataframe into two sub dataframe, below is an example to show how ETL seperate one JSON file into two destination file.



								Song	Artist
		{
		"num_songs": 1,					
		"artist_id": "ARJIE2Y1187B994AB7",	->	Y	Y
		"artist_latitude": null,		->		Y
		"artist_longitude": null,		->		Y
		"artist_location": "",			->		Y
		"artist_name": "Line Renaud",		->		Y
		"song_id": "SOUPIRU12A6D4FA1E1",	->	Y
		"title": "Der Kleine Dompfaff",		->	Y
		"duration": 152.92036,			->	Y
		 "year": 0				->	Y
		}		

### 3.2 log JSON
Function *process_log_file* in etl.py gets data from log json file, after filtering, tranforming, slicing, finally insert it into three tables:
*users, time, songplays*.

For timestamp of log json file, convert it into multiple column: year, month, week, day, hour, dayofweek.

Using below example to show which table data goes to.

Notice for *songplays* there are two columns (SONGID, ARTISTID) are from table *song*, 
for each song plays in log file, if we can find matching information from table *song, artist*, we will insert SONGID, ARTISTID into songplays.


							User	songplays
		{
		"artist": "Survivor",
		"auth": "Logged In",
		"firstName": "Jayden",		->	Y
		"gender": "M",			->	Y
		"itemInSession": 0,
		"lastName": "Fox",		->	Y
		"length": 245.36771,
		"level": "free",		->	Y	Y	
		"location": "New Orleans, LA",	->		Y
		"method": "PUT",
		"page": "NextSong",
		"registration": 1541033612796.0,
		"sessionId": 100,		->		Y
		"song": "Eye Of The Tiger",
		"status": 200,
		"ts": 1541110994796,		->		Y
		"userAgent": "\"Mozilla"\",	->		Y
		"userId": "101"			->	Y	Y
		}
		
		SONGID(from table 'song')	->		Y
		ARTISTID(from table 'song')	->		Y


You can use **test.ipynb** to test whether you insert data into the table, and check whether there is the matching songid in songplays.

--------*This is the End*--------

