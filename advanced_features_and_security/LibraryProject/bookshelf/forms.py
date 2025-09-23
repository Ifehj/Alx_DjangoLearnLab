from django import forms

class ExampleForm(forms.Form):
    """
    A simple example form to demonstrate CSRF protection and safe input handling.
    """
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)