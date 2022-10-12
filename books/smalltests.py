import csv
import sys
import booksdatasource

'''
user will say: 
python3 books.py books searchString
python3 books.py authors searchString
'''

def main():
    if(len(sys.argv) < 1):
        pass
        
    #file = sys.argv[1]

    dataSource = booksdatasource.BooksDataSource("books1.csv")

    #print("the length of datasource books list is", len(dataSource.bookList))
    #print("first book's title is ", dataSource.bookList[0].title, "published in", dataSource.bookList[0].publication_year, "by", 
    #dataSource.bookList[0].authors)
    #print("the length of datasource authors object list is", len(dataSource.authObList))
    #print("the length of the deleted-list of authors is", len(dataSource.authList))
    #print(dataSource.authList)
    #print("first is", dataSource.authObList[0].given_name, "second is", dataSource.authObList[2].given_name, 
    #"last is", dataSource.authObList[21].given_name)
    #print("the length of bookresults is", len(dataSource.bookResults))
    #print("first book is", dataSource.bookResults[0].title, "second is", dataSource.bookResults[1].title, 
    #"last is", dataSource.bookResults[39].title)
    #print(dataSource.bookResults)
    #print(dataSource.authObList)
    # i = 0
    # while i < (len(dataSource.authObList)):
    #     print(dataSource.authObList[i].given_name)
    #     i += 1

    option = sys.argv[1]
    print("your option is", option)

    if(option == "--title" or option =="-t"):
        print("you asked for books by title!")
        booksToPrint = dataSource.books(sys.argv[2], sys.argv[3])
        print("length of results is", len(booksToPrint))
        print("first book is", booksToPrint[0].title)
    # elif(option == "--author" or option == "-a"):
    #     print("you asked for authors!")
    # elif(option == "--years" or option == "-y"):
    #     print("you asked for books by years!")
    # elif(option == "--help" or option =="-h"):
    #     print("you wanted help?")
    # else:
    #     print("that's not a valid option")


main()