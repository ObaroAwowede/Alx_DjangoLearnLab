from django.db import models

class Author(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.title} by {self.author.name}"
        
    
class Library(models.Model):
    name = models.CharField(max_length = 100)
    books = models.ManyToManyField(Book)
    return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length = 100)
    library = models.OneToOneField(
        Library,
        on_delete = models.CASCADE,
        primary_key = True
    )
    return f"{self.name} in {self.library.name}"
