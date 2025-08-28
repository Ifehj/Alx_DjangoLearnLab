>>> b = Book.objects.get(title="1984")
>>> from django.forms.models import model_to_dict
>>> model_to_dict(b)
# {'id': 4, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}