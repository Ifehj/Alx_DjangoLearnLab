>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> model_to_dict(book)
# {'id': 4, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}