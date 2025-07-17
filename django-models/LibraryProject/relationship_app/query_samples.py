import os
import django
from .models import Author, Book, Librarian, Library

def test_data():
    author1 = Author.objects.create(name = "Tolkien")
    author2 = Author.objects.create(name = "J.K Rowling")
    author3 = Author.objects.create(name = "Robert Ludlum")
    
    book1 = Book.objects.create(title = "Lord of the rings", author = author1)
    book2 = Book.objects.create(title = "Harry Potter And The Goblet of Fire", author = author2)
    book3 = Book.objects.create(title = "The Bourne Identity", author = author3)
    
    library1 = Library.objects.create(name ="John Harris Library")
    library2 = Library.objects.create(name ="the library of Ohara")
    
    library1.books.add(book1,book2)
    library2.books.add(book3)
    
    librarian1 = Librarian.objects.create(name = "Obaro", library = library1)
    librarian2 = Librarian.objects.create(name = "Robin", library = library2)
    
def queries():
    ## query for searching for books by a specific author
    try:
        tolkien = Author.objects.get(name ="Tolkien")
        books_by_tolkien = Book.objects.filter(author = tolkien)
        if books_by_tolkien.exists():
            print("Below are the books:")
            for book in books_by_tolkien:
                print(f" - {book.title}")
        else:
            print("Author has no books")
                
    except Author.DoesNotExist:
        print("Author not found")
    
    ##query for listing all books in a library
    # try:
        library_name = "the library of Ohara"
        ohara_library = Library.objects.get(name = library_name)
        books_in_ohara = ohara_library.books.all()

        if books_in_ohara.exists():
            print("The books in the library of Ohana are:")
            for book in books_in_ohara:
                print(f" - {book.title}")
        else:
            print("No books exist in this library")
    
    # except:
    #     print("The library Ohara does not exist")
        
    ## query to retrieve librarian
    
    try:
        library_name = "the library of Ohara"
        ohara_library = Library.objects.get(name = library_name)
        ohara_librarian = ohara_library.librarian
        print(f"The librarian for {ohara_library.name} is {ohara_librarian.name}")
    except ohara_library.DoesNotExist():
        print("This library was not found")
    except ohara_librarian.DoesNotExist():
        print(f"This librarian was not assigned to {ohara_library.name}")
        
