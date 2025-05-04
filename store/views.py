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

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author

# Decorator to check if user is a superuser
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Book, Author

# Decorator for class-based views
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin

# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

# Class-based permission mixin
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_superuser(self.request.user)



@method_decorator(user_passes_test(is_superuser), name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'store/admin/dashboard.html'


@method_decorator(user_passes_test(is_superuser), name='dispatch')
class ManageBooksView(ListView):
    model = Book
    template_name = 'store/admin/book_list.html'
    context_object_name = 'books'


@method_decorator(user_passes_test(is_superuser), name='dispatch')
class AddBookView(View):
    def get(self, request):
        return render(request, 'store/admin/book_form.html')

    def post(self, request):
        title = request.POST['title']
        author_name = request.POST['author']
        price = request.POST['price']
        stock = request.POST['stock']

        author, created = Author.objects.get_or_create(name=author_name)

        Book.objects.create(
            title=title,
            author=author,
            price=price,
            stock=stock
        )
        return redirect('manage_books')


@method_decorator(user_passes_test(is_superuser), name='dispatch')
class EditBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        authors = Author.objects.all()
        return render(request, 'store/admin/book_form.html', {'book': book, 'authors': authors})

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.title = request.POST['title']
        author_id = request.POST['author']
        book.author = get_object_or_404(Author, pk=author_id)
        book.price = request.POST['price']
        book.stock = request.POST['stock']
        book.save()
        return redirect('manage_books')


@method_decorator(user_passes_test(is_superuser), name='dispatch')
class DeleteBookView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return redirect('manage_books')


@method_decorator(user_passes_test(is_superuser), name='dispatch')
class CustomAdminDashboardView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, "store/admin_dashboard.html", {"books": books})


@method_decorator(login_required, name='dispatch')
class AccountSettingsView(TemplateView):
    template_name = 'store/account_settings.html'



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
