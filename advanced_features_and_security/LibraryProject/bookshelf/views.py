from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book


@permission_required('yourapp.can_view', raise_exception=True)
def book_list(request):
   return HttpResponse("You can VIEW books.")

@permission_required('yourapp.can_create', raise_exception=True)
def book_create(request):
    return HttpResponse("You can CREATE a book.")


@permission_required('yourapp.can_edit', raise_exception=True)
def book_edit(request, book_id):
    return HttpResponse(f"You can EDIT book with ID {book_id}.")


@permission_required('yourapp.can_delete', raise_exception=True)
def book_delete(request, book_id):
    return HttpResponse(f"You can DELETE book with ID {book_id}.")
