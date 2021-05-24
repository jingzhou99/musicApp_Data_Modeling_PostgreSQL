# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id SERIAL PRIMARY KEY, 
    start_time bigint NOT NULL, 
    user_id int NOT NULL, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int NOT NULL, 
    location varchar, 
    user_agent varchar
);
""")

user_table_create = ("""
CREATE TABLE users (
    user_id int PRIMARY KEY, 
    first_name varchar(20) NOT NULL, 
    last_name varchar(20) NOT NULL, 
    gender varchar(5), 
    level varchar
);
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id varchar PRIMARY KEY, 
    title varchar NOT NULL, 
    artist_id varchar, 
    year int, 
    duration numeric(9,5)
);
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id varchar PRIMARY KEY, 
    name varchar NOT NULL, 
    location varchar, 
    latitude numeric(8,5), 
    longitude numeric(8,5)
);
""")

time_table_create = ("""
CREATE TABLE time (
    start_time bigint PRIMARY KEY, 
    hour int2, 
    day int2, 
    week int2, 
    month int2, 
    year int2, 
    weekday int2
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location, 
    user_agent
    ) 
VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
""")

user_table_insert = ("""
INSERT INTO users (
    user_id, 
    first_name, 
    last_name, 
    gender, 
    level
    ) 
VALUES(%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""")

song_table_insert = ("""
INSERT INTO songs (
    song_id,
    title, 
    artist_id, 
    year, 
    duration
    ) 
VALUES(%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (
    artist_id, 
    name, 
    location, 
    latitude, 
    longitude
    ) 
VALUES(%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time (
    start_time , 
    hour, 
    day, 
    week, 
    month, 
    year, 
    weekday
    ) 
VALUES(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, 
       a.artist_id 
  FROM songs AS s
  JOIN artists AS a ON s.artist_id = a.artist_id
 WHERE (title = %s) and (duration = %s) and (name = %s)
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]