'''
    Sophia Wang

    convert.py
    starter code from Jeff Ondich, 15 Oct 2021
    Started in class, polished later

    Illustrating how to use Python dictionaries, etc. to
    start converting the data. This is based on the Kaggle
    Olympics data, and assumes you have a copy of the
    athlete_events.csv file.

    In this small example, I am imagining three tables as shown
    below. The point of this code sample is to illustrate how you
    could connect the event_results table's ID fields to the
    appropriate IDs in the athletes and events tables.

    # Like "Simone Arianne Biles"
    CREATE TABLE athletes (
        id INTEGER,
        name TEXT
    );

    # Like "Gymnastics Women's Individual All-Around"
    CREATE TABLE events (
        id INTEGER,
        name TEXT
    );

    # One row represents one athlete competing in one event
    # at one time.
    CREATE TABLE event_results (
        athlete_id INTEGER,
        event_id INTEGER,
        medal TEXT
    );

    When I run this code, I end up with three new files: athletes.csv,
    events.csv, and event_results.csv. One of the lines of athletes.csv is:

        11495,Simone Arianne Biles

    One of the rows in events.csv is:

        213,Gymnastics Women's Individual All-Around

    And one of the rows in event_results.csv is:

        11495,213,Gold

    When you combine those three rows from three different tables, you can
    conclude that Simone Biles won the Gold medal in the
    Gymnastics Women's Individual All-Around. This sample program hasn't
    included year information or city information or anything like that.
    But I hope this code helps you understand one way to approach converting
    raw data into structured tabular data.
'''

import csv

# Strategy:
# (1) Create a dictionary that maps athlete IDs to athlete names
#       and then save the results in athletes.csv
# (2) Create a dictionary that maps event names to event IDs
#       and then save the results in events.csv
# (3) For each row in the original athlete_events.csv file, build a row
#       for our new event_results.csv table
#
# NOTE: I'm doing these three things in three different passes through
# the athlete_events.csv files. This is not necessary--you can do it all
# in a single pass.


# (1) Create a dictionary that maps athlete_id -> athlete_name
#       and then save the results in athletes.csv
athletes = {}
with open('athlete_events.csv') as original_data_file,\
        open('athletes.csv', 'w') as athletes_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(athletes_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file

    #Athlete height, weight seems to be consistent in kaggle csv files. 
    #However, I don't think those heights/weights are accurate to each game, event, etc. Therefore I choose to leave them out
    #Also, names are inconsistent and messy between athletes from different cultures. I choose not to split it into given 
    #and surname or some equivalent
    for row in reader:
        athlete_id = row[0]
        athlete_name = row[1]
        if athlete_id not in athletes:
            athletes[athlete_id] = athlete_name
            writer.writerow([athlete_id, athlete_name])

# (2) Create a dictionary that maps event_name -> event_id
#       and then save the results in events.csv
events = {}
with open('athlete_events.csv') as original_data_file,\
        open('events.csv', 'w') as events_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(events_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file

    #Note: all the events also contain the category name in the beginning, like "Swimming Women's"
    #Thus a category column is unnecessary 
    for row in reader:
        event_name = row[13]
        if event_name not in events:
            event_id = len(events) + 1
            events[event_name] = event_id
            writer.writerow([event_id, event_name])


games = {}
with open('athlete_events.csv') as original_data_file,\
    open('games.csv', 'w') as games_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(games_file)
    heading_row = next(reader)
    for row in reader:
        game_combined = row[8]
        game_year = row[9]
        game_season = row[10]
        game_city = row[11]

        #game_combined used only to check for duplicates and for linking table
        if game_combined not in games:
            game_id = len(games) + 1
            games[game_combined] = game_id
            writer.writerow([game_id, game_year, game_season, game_city])

nocs = {}
with open('noc_regions.csv') as original_data_file,\
        open('nocs.csv', 'w') as nocs_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(nocs_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        noc_abbreviation = row[0]
        noc_name = row[1]

        #singapore discrepancy in abbreviations, I go with SGP
        if noc_abbreviation == 'SIN':
            noc_abbreviation = 'SGP' 
        if noc_name not in nocs:
            noc_id = len(nocs) + 1
            nocs[noc_abbreviation] = noc_id
            writer.writerow([noc_id, noc_abbreviation, noc_name])


# (3) For each row in the original athlete_events.csv file, build a row
#       for our new event_results.csv table
with open('athlete_events.csv') as original_data_file,\
        open('event_results.csv', 'w') as event_results_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(event_results_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        athlete_id = row[0]
        event_name = row[13]
        event_id = events[event_name] # this is guaranteed to work by section (2)
        noc_abbreviation = row[7]
        noc_id = nocs[noc_abbreviation]
        game_combined= row[8]
        game_id = games[game_combined]
        medal = row[14]
        writer.writerow([athlete_id, event_id, noc_id, game_id, medal])

