from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Book
from django.shortcuts import  get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

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
