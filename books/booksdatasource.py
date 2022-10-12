#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.authList= list() #can make these sets which don't allow duplicates but different methods for those
        self.bookList = list()
        #self.overall = list()
        currBook = list()
        with open(books_csv_file_name) as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                #currBook = list()
                #print("new row")

                i = 0
                while i < len(row):
                    #print("adding", row[i], "to currbook")
                    currBook.append(row[i]) #add title, pubyear, author
                    #print("i is", i)
                    if (i == 2): #last item in row, should be author
                        newBookAuthors = list()
                        #print("last one!")
                        #print("currbook[2] is", currBook[2])
                        newBookAuthors.append(currBook[2])
                        #print("newBookAuthors contains", newBookAuthors[0])
                        newBook = Book(currBook[0], currBook[1], newBookAuthors)
                        #print("newbook's authors are", newBook.authors)
                         #all done with bookinfo, add it to total list
                        #print(row[i])
                        self.authList.append(row[i]) #add author info to authlist

                        self.bookList.append(newBook)
                        while len(currBook) > 0: #clear it out
                            #print("popping")
                            currBook.pop()

                    i += 1

        self.authObList = list()

        authIndex = 0
        while authIndex < len(self.authList):
            print("index is", authIndex, "and author is", self.authList[authIndex])
            if authIndex < (len(self.authList) - 1):
                print("next one is", self.authList[authIndex + 1])
            if authIndex > 0:
                print("prev is", self.authList[authIndex-1])
            #for auth in self.authList:
            #print("new loop, authList is", self.authList)
            #print(self.authList[authIndex])
            authSplit = self.authList[authIndex].split()
            #print(authSplit)

            i = 1
            surname = ""
            while i <= len(authSplit) -2:
                surname += authSplit[i]
                if i < len(authSplit) -2:
                    surname += " "
                i += 1
            print(surname)

            listAuthYear = authSplit[len(authSplit) - 1]
            listAuthYear = listAuthYear.strip("()")
            listAuthYear = listAuthYear.split("-")
            #print(listAuthYear)
            #print("making authOb")
            authOb = Author(surname, authSplit[0], listAuthYear[0], listAuthYear[1])

            #print("author is", authOb.given_name, authOb.surname)

            checkString = authOb.given_name + " " + authOb.surname + " (" + authOb.birth_year + "-" + authOb.death_year + ")"

            self.authObList.append(authOb)
            #print("appended", authSplit[0])

            #skipCount = 0;
            if checkString in self.authList:
                #print("in authList")
                while checkString in self.authList:
                    self.authList.remove(checkString)
                    #skipCount += 1
                    #print("removed", checkString)

            # self.bookResults = list()
            # self.bookResults = self.bookList
            # self.bookResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))

            # if skipCount >= 1:
            #     authIndex -= 1
            # authIndex += 1

            #print("checkString is", checkString)
            # if "Connie Willis (1945-)" in self.authList:
            #     print("found match")
            
            # if checkString == "Connie Willis (1945-)":
            #     print("checkstring matches")

            # if checkString not in self.authList:
            #     print(checkString, "not in list")
            #     self.authObList.append(authOb)
            # if checkString not in self.authList:
            #     print("did not match")
            #     self.authObList.append(authOb)

            



        # listAuthYear = authSplit[len(authSplit) - 1]
        # listAuthYear = listAuthYear.strip("()")
        # listAuthYear = listAuthYear.split("-")

        # i = 1
        # surname = ""
        # while i <= len(authSplit) -2:
        #     surname += authSplit[i]
        #     if i < len(authSplit) -2:
        #         surname += " "
        #     i += 1

        # auth = Author(surname, authSplit[0], listAuthYear[0], listAuthYear[1])
        # self.authList.append(auth)

        # while len(authSplit) > 0:
        #     authSplit.pop()
            
        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''

        return []

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        bookResults = list()

        if(search_text == None):
            bookResults = self.bookList
            return bookResults
            
        searchLower = search_text.lower()
            

        for book in self.bookList:
            titleLower = book.title.lower()
            if searchLower in titleLower:
                bookResults.append(book)


        #Since I don't remember how to sort by attribute, I looked up it up and found https://runestone.academy/ns/books/published/fopp/Sorting/SecondarySortOrder.html
        if sort_by.lower() == "year":
            bookResults.sort(key = lambda bookOb: (bookOb.publication_year, bookOb.title))
            return bookResults
        else:
            bookResults.sort(key = lambda bookOb: (bookOb.title, bookOb.publication_year))
            return bookResults

        return []

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        return []

