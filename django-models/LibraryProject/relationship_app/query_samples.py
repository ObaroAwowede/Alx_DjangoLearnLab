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
        author_name = "Tolkien"
        author = Author.objects.get(name=author_name)
        books_by_tolkien = objects.filter(author=author)
        if books_by_tolkien.exists():
            print("Below are the books:")
            for book in books_by_tolkien:
                print(f" - {book.title}")
        else:
            print("Author has no books")
                
    except Author.DoesNotExist:
        print("Author not found")
        

    library_name = "the library of Ohara"
    ohara_library = ""
    
    try:
        ohara_library = Library.objects.get(name=library_name)
        books_in_ohara = ohara_library.books.all()

        if books_in_ohara.exists():
            print(f"The books in {ohara_library.name} are:")
            for book in books_in_ohara:
                print(f" - {book.title}")
        else:
            print(f"No books exist in {ohara_library.name}.")

    except Library.DoesNotExist:
        print(f"The library '{library_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred while fetching the library or books: {e}")

    if ohara_library: 
        try:
            ohara_librarian = Librarian.objects.get(library=ohara_library)
            print(f"The librarian for {ohara_library.name} is {ohara_librarian.name}.")
        except Librarian.DoesNotExist:
            
            print(f"No librarian was found for {ohara_library.name}.")
        except Exception as e:
            print(f"An unexpected error occurred while fetching the librarian: {e}")
    else:
        print(f"Cannot retrieve librarian because the library '{library_name}' was not found in the previous step.")
    