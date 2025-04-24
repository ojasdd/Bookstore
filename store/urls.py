from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.CartView.as_view(), name='view-cart'),
    path('custom-admin/', views.CustomAdminView.as_view(), name='custom-admin'),
]
