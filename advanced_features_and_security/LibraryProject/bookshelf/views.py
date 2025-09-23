from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm
from django.shortcuts import render

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

def example_form_view(request):
    """
    Simple view to demonstrate CSRF protection and safe form handling.
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            # Safe handling: using cleaned_data avoids SQL injection / unsafe strings
            return HttpResponse(f"Form submitted successfully! Hello {name}, your email is {email}")
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})