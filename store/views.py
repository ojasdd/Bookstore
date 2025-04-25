from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Book
from django.shortcuts import  get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Book  # Assuming you're managing the Book model here
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book
from django.shortcuts import render, redirect
from .models import Book
from django.http import HttpResponse
from django.urls import reverse
# core/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Book # Replace with your actual models
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author

def admin_dashboard(request):
    return render(request, 'store/admin/dashboard.html')

def manage_books(request):
    books = Book.objects.all()
    return render(request, 'store/admin/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author_name = request.POST['author']  # Text input for author name
        price = request.POST['price']
        stock = request.POST['stock']

        # Check if author exists, otherwise create new author
        author, created = Author.objects.get_or_create(name=author_name)

        # Create the book
        Book.objects.create(
            title=title,
            author=author,
            price=price,
            stock=stock
        )
        return redirect('manage_books')  # Redirect to the books management page
    
    # For GET request, render the form
    return render(request, 'store/admin/book_form.html')

def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = Author.objects.all()
    if request.method == 'POST':
        book.title = request.POST['title']
        author_id = request.POST['author']
        book.author = get_object_or_404(Author, pk=author_id)
        book.price = request.POST['price']
        book.stock = request.POST['stock']
        book.save()
        return redirect('manage_books')
    return render(request, 'store/admin/book_form.html', {'book': book, 'authors': authors})

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('manage_books')


def custom_admin_dashboard(request):
    books = Book.objects.all()
    return render(request, "store/admin_dashboard.html", {"books": books})


@login_required
def account_settings(request):
    return render(request, 'store/account_settings.html')


class CustomLogoutView(LogoutView):
    next_page = '/login/'  # Redirect after logout


class CustomLoginView(LoginView):
    template_name = 'store/login.html'


class CustomAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'store/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser  # only superusers can access


class AddToCartView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        cart = request.session.get('cart', {})
        cart[str(book.pk)] = cart.get(str(book.pk), 0) + 1
        request.session['cart'] = cart
        return redirect('book-list')

from django.shortcuts import render

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        books = Book.objects.filter(pk__in=cart.keys())
        cart_items = []
        total = 0
        for book in books:
            quantity = cart[str(book.pk)]
            total += book.price * quantity
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': book.price * quantity
            })
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'store/book_list.html', {'books': books})

class RegisterView(View):
    def get(self, request):
        return render(request, 'store/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'store/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book-list')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
