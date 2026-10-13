from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'genre',
            'published_year',
            'isbn',
            'description',
            'cover_image',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: The Alchemist',
                }
            ),
            'author': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Paulo Coelho',
                }
            ),
            'genre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Fiction',
                }
            ),
            'published_year': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 1988',
                }
            ),
            'isbn': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 9780061122415',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Write a short description of this book...',
                }
            ),
            'cover_image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*',
                }
            ),
        }
        