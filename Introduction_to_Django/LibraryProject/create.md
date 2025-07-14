## Creating a book instance
<p>How to create an instance of a book class</p>

<ul>
    <p>Import Book from models</p>
    <p>Create an object, (instantiating the class)</p>
    <p>Fill necessary parameters</p>
    <p>Save the book</p>
</ul>

<p>Code:</p>
<div>
    from bookshelf.models import Book

    book1 =Book(
        title="1984",
        author ="George Orwell",
        publication_year = 1984
    )

    book1.save()
</div>