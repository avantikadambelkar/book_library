from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm
from django.db.models import Count
from django.shortcuts import redirect

def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "library/landing.html")

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return redirect("home")  # your existing public gallery

@login_required
def dashboard(request):
    total_books = Book.objects.count()
    genres_qs = Book.objects.values("genre").annotate(cnt=Count("id")).order_by("-cnt")
    total_genres = Book.objects.values("genre").distinct().count()
    recent_books = Book.objects.order_by("-id")[:6]  # last 6 added

    return render(request, "library/dashboard.html", {
        "total_books": total_books,
        "total_genres": total_genres,
        "genres": genres_qs,
        "recent_books": recent_books,
    })


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

    genres = (
        Book.objects.values_list("genre", flat=True)
        .distinct()
        .order_by("genre")
    )

    return render(
        request,
        "library/home.html",
        {
            "books": books,
            "genres": genres,
            "current_query": query,
            "current_genre": genre,
        },
    )


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'library/book_form.html', {
        'form': form,
        'page_title': 'Add a new book',
        'button_text': 'Save book',
    })


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {
        'form': form,
        'page_title': 'Edit book',
        'button_text': 'Save changes',
    })


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})


@login_required
def book_bulk_create(request):
    BookFormSet = modelformset_factory(
        Book,
        form=BookForm,
        extra=5,
        max_num=10,
        validate_max=True,
    )

    if request.method == 'POST':
        formset = BookFormSet(
            request.POST,
            request.FILES,
            queryset=Book.objects.none(),
        )

        if formset.is_valid():
            books = formset.save(commit=False)

            for book in books:
                if book.title and book.author:
                    book.save()

            return redirect('book_list')
    else:
        formset = BookFormSet(queryset=Book.objects.none())

    return render(request, 'library/book_bulk_form.html', {
        'formset': formset,
    })
