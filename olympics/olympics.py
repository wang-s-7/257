#!/usr/bin/env python3
'''
    Sophia Wang

    starter code taken from:
    psycopg2-sample.py
    Jeff Ondich, 23 April 2016
    A very short, demo of how to use psycopg2 to connect to
    and query a PostgreSQL database. This demo assumes a "books"
    database like the one I've used in CS257 for the past few years,
    including an authors table with fields
        (id, given_name, surname, birth_year, death_year)
    You might also want to consult the official psycopg2 tutorial
    at https://wiki.postgresql.org/wiki/Psycopg2_Tutorial.
    Also, SEE THE NOTE BELOW ABOUT config.py. It's important.
'''
import sys
import psycopg2
import config
import sys



def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password,
                                port=config.port)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def get_noc_athletes(search_text):
    ''' Returns a list of the full names of all the athletes
        in a particular NOC, ordered by the name that appears 
        first on official documents. '''
    athletes = []
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        #checks if it's an abbreviation
        if len(search_text) == 3:
            # Execute the query
            query = '''SELECT DISTINCT athletes.name 
                        FROM athletes, nocs, event_results 
                        WHERE athletes.id = event_results.athlete_id
                        AND nocs.id = event_results.noc_id
                        AND nocs.abbreviation ILIKE %s'''
            cursor.execute(query, (search_text,))



        #otherwise must be full NOC name
        else:
            # Execute the query
            query =  '''SELECT DISTINCT athletes.name 
                        FROM athletes, nocs, event_results 
                        WHERE athletes.id = event_results.athlete_id
                        AND nocs.id = event_results.noc_id
                        AND nocs.name ILIKE %s'''
            cursor.execute(query, (search_text,))

        # Iterate over the query results to produce the list of athlete names.
        for row in cursor:
            name = row[0]
            athletes.append(f'{name}')


    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_medals_overall(search_text):
    ''' Returns a list of all of the countries who have earned at least
        one medal of type search_text (which can be bronze, silver, or gold,
        but only one of those), sorted in descending order of # of medals
        earned.

        This function introduces an important security issue. Suppose you
        have information provided by your user (e.g. a search string)
        that needs to become part of your SQL query. Since you can't trust
        users not to be malicious, nor can you trust them not to do weird and
        accidentally destructive things, you need to be very careful about
        how you use any input they provide. To avoid the very common and
        very dangerous security attack known as "SQL Injection", we will use
        the parameterized version of cursor.execute whenever we're using
        user-generated data. See below for how that goes. '''
    nocs_medals = []
    
    connection = get_connection()
    cursor = connection.cursor()


    try:
        #total medals, unspecified
        if search_text == None:
            query = '''SELECT COUNT(event_results.medal), nocs.name
                    FROM nocs, event_results
                    WHERE nocs.id = event_results.noc_id
                    AND event_results.medal IS NOT NULL
                    GROUP BY nocs.name
                    ORDER BY COUNT(event_results.medal) DESC'''
            
            cursor.execute(query, (search_text,))

        #type of medal is specified
        else:
            query = '''SELECT COUNT(event_results.medal), nocs.name
                    FROM nocs, event_results
                    WHERE nocs.id = event_results.noc_id
                    AND event_results.medal ILIKE %s
                    GROUP BY nocs.name
                    ORDER BY COUNT(event_results.medal) DESC'''

            cursor.execute(query, (search_text,))

        for row in cursor:
            medals = row[0]
            noc_name = row[1]
            nocs_medals.append(f'{noc_name}: {medals}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return nocs_medals

def get_matching_athletes(search_text):
    ''' Returns a list of the full names of all athletes in the database
        whose names contain (case-insensitively) the specified search string. '''
        
    athletes = []
    try:
        query = '''SELECT DISTINCT athletes.name, nocs.name
                FROM athletes, nocs, event_results
                WHERE athletes.id = event_results.athlete_id
                AND nocs.id = event_results.noc_id
                AND athletes.name ILIKE CONCAT('%%', %s, '%%')
                AND event_results.medal IS NOT NULL
                ORDER BY athletes.name'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            athlete = row[0]
            noc = row[1]
            athletes.append(f'{athlete} | {noc}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes



def main():

    if len(sys.argv) < 2:
        raise SyntaxError('Too few arguments, type python3 olympics.py -h for help')
        return

    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        usage = open('usage.txt')
        print(usage.read())
        usage.close()
        return

    elif sys.argv[1] == 'noc-athletes':
        if len(sys.argv) < 3:
            raise SyntaxError('Must provide a NOC to filter by')
        else:
            search_text = sys.argv[2]
            print(f'========== All athletes from {search_text} ==========')
            athletes_list = get_noc_athletes(search_text)
            for athlete in athletes_list:
                print(athlete)

    elif sys.argv[1] == 'medals-overall':
        if len(sys.argv) == 2:
            search_text = None
            print(f'========== Countries sorted by total medals ==========')
            medals_list = get_medals_overall(search_text)
            for noc in medals_list:
                print(noc)
        else:
            search_text = sys.argv[2]
            print(f'========== Countries sorted by total {search_text} medals ==========')
            medals_list = get_medals_overall(search_text)
            for noc in medals_list:
                print(noc)

    elif sys.argv[1] == 'search-athletes':
        if len(sys.argv) < 3:
            raise SyntaxError('Must provide a string to filter by')
        else:
            search_text = sys.argv[2]
            print(f'========== Results of athletes whose surnames contain "{search_text}" ==========')
            athletes_list = get_matching_athletes(search_text)
            for athlete in athletes_list:
                print(athlete)

    else:
        raise SyntaxError('Invalid command, type python3 olympics.py -h for help')





if __name__ == '__main__':
    main()