from django.urls import path
from . import views
from .views import feedback_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('feedback/', feedback_view, name='feedback'),
    path('place_order/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
]
