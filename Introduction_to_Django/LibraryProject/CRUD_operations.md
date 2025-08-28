# CRUD Operations

## Create
```python
from bookshelf.models import Book

book1 = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book1
# <Book: 1984 by George Orwell (1949)>

from django.forms.models import model_to_dict

book = Book.objects.get(title="1984")
model_to_dict(book)
# {'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell (1949)>

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# (1, {'bookshelf.Book': 1})

Book.objects.all()
# <QuerySet []>

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# (1, {'bookshelf.Book': 1})

Book.objects.all()
# <QuerySet []>
