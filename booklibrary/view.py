from django.db.models import Q
from django.shortcuts import render
from .models import Book

def home(request):
    books = Book.objects.all()
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    if genre:
        books = books.filter(genre__iexact=genre)

    # Get list of all genres for the dropdown
    genres = (
        Book.objects.values_list("genre", flat=True)
        .distinct()
        .order_by("genre")
    )

    return render(
        request,
        "booklibrary/home.html",
        {"books": books, "genres": genres, "current_query": query, "current_genre": genre},
    )