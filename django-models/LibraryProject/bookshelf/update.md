## Update Attributes of Book
<p>How to update information about the book:</p>
<p>Code:</p>
<div>
    from bookshelf.models import Book

    book1 =Book.objects.create(
        title="1984",
        author ="George Orwell",
        publication_year = 1984
    )

    book = Book.objects.get(title="1984")
    book.title = "Nineteen Eighty-Four"
    book.save()
</div>