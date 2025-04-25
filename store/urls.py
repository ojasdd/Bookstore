from django.urls import path
from . import views
from .views import CustomLoginView
from .views import admin_dashboard
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/books/', views.manage_books, name='manage_books'),
    path('admin-panel/books/add/', views.add_book, name='add_book'),
    path('admin-panel/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('admin-panel/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Cart
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.CartView.as_view(), name='view-cart'),

    # Account
    path('account/', views.account_settings, name='account-settings'),

    # Add Book
    path('add-book/', views.add_book, name='add-book'),
]