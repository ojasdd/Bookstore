from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    
    # Admin
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/books/', views.ManageBooksView.as_view(), name='manage_books'),
    path('admin/books/add/', views.AddBookView.as_view(), name='add_book'),
    path('admin/books/edit/<int:book_id>/', views.EditBookView.as_view(), name='edit_book'),
    path('admin/books/delete/<int:book_id>/', views.DeleteBookView.as_view(), name='delete_book'),
    
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Keep Django's default logout
    
    # Cart
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.CartView.as_view(), name='view-cart'),
    
    # Account
    path('account/', views.AccountSettingsView.as_view(), name='account-settings'),

    # Extra (if you still use it)
    path('add-book/', views.AddBookView.as_view(), name='add-book'),
]