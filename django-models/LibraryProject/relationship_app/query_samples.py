from relationship_app.models import Author, Book, Library, Librarian
# Sample Queries

def get_books_by_author(author_name):
	try:
		author = Author.object.get(name=author_name)
		books = author.books.all()
		print(f"Books by {author_name}: {[book.title for book in books]}")
	except Author.DoesNotExist:
		print(f"No author found with name {author_name}")

def get_books_in_library(library_name):
	try:
		library = Library.objects.get(name=library_name)
		books = library.books.all()
		print(f"Books in {library_name}: {[book.title for book in books]}")
	except Library.DoesNotExist:
		print(f"No library found with name {library_name}")

def get_librarian_for_library(library_name):
	try:
		library = Library.objects.get(name=library_name)
		librarian = library.librarian
		print(f"Librarian for {library_name}: {librarian.name}")
	except Library.DoesNotExist:
		print(f"No library found with name {library_name}")

if __name__ == "__main__":
    # Example usage
    get_books_by_author("J.K. Rowling")
    get_books_in_library("Central Library")
    get_librarian_for_library("Central Library")