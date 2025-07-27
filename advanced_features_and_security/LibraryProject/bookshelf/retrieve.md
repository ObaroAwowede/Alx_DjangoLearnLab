## Retrieving attributes of a book
<p>How to retrieve information about the book:</p>
<p>Code:</p>
<div>
    from bookshelf.models import Book

    book1 =Book.objects.create(
        title="1984",
        author ="George Orwell",
        publication_year = 1984
    )

    b = Book.objects.get(pk=book1.pk)
    print(/n"The title of this book is: ",b.title)
    print(/n"The author of this book is: ",b.author)
    print(/n"It was published in the year: "b.publication_year)
</div>