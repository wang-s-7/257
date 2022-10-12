#Ariana Borlak, Sophia Wang

'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    #tests for books
    def test_all_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Neverwhere')
        self.assertTrue(books[2].title == 'Omoo')
    
    def test_unique_book(self):
        books = self.data_source.books('1q84')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].title == '1Q84')
       
    def test_no_book(self):
        books = self.data_source.books('jaskfldjfa')
        self.assertTrue(len(books) == 0)

    #tests for author
    def test_all_authors(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors()
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0].title == 'Austen', 'Jane')
        self.assertTrue(authors[1].title == 'Gaiman', 'Neil')
        self.assertTrue(authors[2].title == 'Melville', 'Herman')

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))
    
    def test_multiple_author(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë', 'Ann'))
        self.assertTrue(authors[1] == Author('Brontë', 'Charlotte'))
        self.assertTrue(authors[2] == Author('Brontë', 'Emily'))

    def test_no_author(self):
        authors=self.data_source.authors('asdfkjl;')
        self.assertTrue(len(authors) == 0)

    #tests for year
    def test_all_years(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books_between_years()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Omoo')
        self.assertTrue(books[2].title == 'Neverwhere')

    def test_unique_year(self):
        books = self.data_source.books_between_years('1813', '1813')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].title == 'Sense and Sensibility')

    def test_multiple_year(self):
        books = self.data_source.books_between_years('2019', '2019')
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'There, There')
        self.assertTrue(books[1].title == 'All Clear')
        self.assertTrue(books[2].title == 'Fine, Thanks')

    def test_no_year(self):
        #testing wrong order (greater first, lesser second) doesn't work because we want it to reorder it always
        books = self.data_source.books_between_years('1814', '1814')
        self.assertTrue(len(books) == 0)
    
    def test_first_none(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books_between_years('None','1850')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Omoo')

    def test_second_none(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books_between_years('1900','None')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0].title == 'Neverwhere')

    def test_both_none(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books_between_years('None', 'None')
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0] == Book('Emma'))
        self.assertTrue(books[1] == Book('Omoo'))
        self.assertTrue(books[2] == Book('Neverwhere'))

#figure out what to do in terms of testing for no string/print all authors
#all case insensitive results show up, diacritics show up when you search without them
#books testing: putting in gibberish for sortby still gives you default sorting/no type error
#books testing: zero books, one book, two+ books, all books, check sorting (btwn 2/all)
#booksbetween testing: if start year > end year, return nothing; zero, one, two, all, checking none for both start and
#check that book results are returned in sorted order by pub year
#check if user sort option works

if __name__ == '__main__':
    unittest.main()

