import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, datafile):
    """
    Description: 
    Read one JSON file into a Pandas dataframe
    Slice the dataframe, then, insert data to table "song" and "artist" 
    by using given database cursor.
    
    Args:
        cur: the cursor object
        datafile: string contains the path and name of a JSON file
    Return:
        None
    """
    # open song file
    df = pd.read_json(datafile, lines=True)

    # insert song record
    song_data = list(df[['song_id','title','artist_id','year','duration']].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id','artist_name','artist_location',\
                           'artist_latitude','artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, datafile):
    """
    Description: 
    Read one JSON file into a Pandas dataframe;
    Slice the dataframe, filtering and slicing
    Insert data to table "time";
    Insert data to table "user";
    Insert data to table "songplays", before each insert operation, try to find the songid and artistid 
    in song and artist table.
        
    Args:
        cur: cursor of the target database, where data flows to
        datafile: string contains the path and name of a JSON file
    Return:
        None
    """
    # open log file
    df = pd.read_json(datafile, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.dayofweek)
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame({
                            'timestamp': df['ts'], 
                            'hour': t.dt.hour, 
                            'day': t.dt.day, 
                            'week': t.dt.week, 
                            'month': t.dt.month, 
                            'year': t.dt.year, 
                            'weekday': t.dt.dayofweek
                            })

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.length, row.artist))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, \
                         row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description:
    Walk through the designated folder, matching all the JSON file, 
    and return a string list in the format of "filepath"+"json file name".
    
    Loop each Json file, and in the loop, call another function ('func' as args) 
    to process each Json file.
    
    Args:
        cur: database cursor
        conn: database connection
        filepath: filepath of source data files
        func: name of another function
    Return:
        None
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):  # index starts from 1, instead of 0
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Connect to the sparkify database, and get the cursor
    
    Call function 'process_data' to process song file
    Call function 'process_data' to process user's log file (user's activities)
    
    Close connection to database
    """
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()