import sys

class Book:
    def __init__(self, name, author, isbn, year):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.year = year

def getUserChoice():
    choice = input('''
    Welcome to the Library Database.
    What action will you like to perform?
    
    1) Add new book
    2) Print current database content
    Q) Exit the program

    ''')
    while True:
        if choice not in ['1', '2', 'Q', 'q']:
            choice = input("Please enter a valid input: ")
        else:
            break
    return choice

def getBookFromUser():
    '''Asks the user for the name, author, isbn and publishing year of the book
    and returns a Book object.
    It can also return a None object if the user decides not to add new book.'''

    name = input("Enter the name of the book: ")
    author = input("Enter the name of the author: ")
    isbn = input("Enter the ISBN of the book: ")
    year = input("Enter the publishing year of the book: ")

    confirmation = input('''
            Are you sure you want to add new book:
            Name: %s
            Author: %s
            ISBN: %s
            Year: %s,

            Y/N
            ''' % (name, author, isbn, year))
    if confirmation in ['Y', 'y']:
        book = Book(name, author, isbn, year)
        return book
    return None
            
def convertBookEntryToBook(book_entry):
    '''Converts a Book entry to a Book object and returns Book object'''
    book_entry = book_entry.strip()
    book_entry = book_entry.split('/')
    book = Book(book_entry[0], book_entry[1], book_entry[2], book_entry[3])
    return book

def convertBookToBookEntry(book):
    '''Converts a Book object to a saveable Book entry.'''
    book_entry = '/'.join([book.name, book.author, book.isbn, book.year]) + '\n'
    return book_entry

def readBookEntriesFromFile(file):
    '''Converts each book entry in the file to a Book object
    and returns a list of Book objects'''
    with open(file) as f:
        book_entries = f.readlines()
    books = list(map(convertBookEntryToBook, book_entries))
    return books

def addBookToBooks(book, books):
    '''Adds a Book object to a list of Book objects while
    maintaining the order.
    Returns the updated list of Book objects.'''
    book_created = False
    
    for i in range(len(books)):
        if int(book.year) < int(books[i].year):
            books = books[:i] + [book] + books[i:]
            book_created = True
            break
    if not book_created:
        books += [book]
    return books

def saveBooksToFile(books, file):
    '''Save books to file after converting them to book entries.'''
    book_entries = list(map(convertBookToBookEntry, books))
    with open(file, 'w') as f:
        for book_entry in book_entries:
            f.write(book_entry)

def printBooks(books):
    '''Print the list of books in a pretty format.'''
    name_column = 30
    author_column = 30
    isbn_column = 20
    year_column=5
    for book in books:
        if len(book.name) > name_column:
            name_column = len(book.name) + 5
        if len(book.author) > author_column:
            author_column = len(book.author) + 5
    h_len = name_column + author_column + isbn_column + year_column + 4
    padding = ' '
    print('_' * h_len)
    print('NAME'.rjust(name_column, padding) \
        + '|' + 'AUTHOR'.rjust(author_column, padding) \
            + '|' + 'ISBN'.rjust(isbn_column, padding) \
                + '|' + 'YEAR'.rjust(year_column, padding) + '|')
    print('_' * h_len)
    for book in books:
        print(book.name.rjust(name_column, padding) \
            + '|' + book.author.rjust(author_column, padding) \
                + '|' + book.isbn.rjust(isbn_column, padding) \
                     + '|' + book.year.rjust(year_column, padding) + '|')
    print('_' * h_len)

if __name__ == "__main__":
    try:
        library_file = sys.argv[1]
    except IndexError:
        print("Error: File was not provided")
        sys.exit()
    
    books = readBookEntriesFromFile(library_file)
    while True:
        choice = getUserChoice()
        if choice == '1':
            book = getBookFromUser()
            if not book:
                continue 
            books = addBookToBooks(book, books) 
            saveBooksToFile(books, library_file)
        elif choice == '2':
            printBooks(books)
        else:
            break