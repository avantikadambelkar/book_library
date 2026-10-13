from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.root_redirect, name="root"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("home/", views.home, name="home"),

    path("books/", views.book_list, name="book_list"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path("book/new/", views.book_create, name="book_create"),
    path("book/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("book/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/bulk-add/", views.book_bulk_create, name="book_bulk_create"),
]