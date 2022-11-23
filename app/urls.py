from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config/', views.stripe_config),
    path('add/', views.add, name="add"),
    path('add/add-product', views.add_product, name='add-product'),
    path('checkout/', views.checkout,
         name='checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:id>', views.remove_cart, name='remove_cart'),
    path('cart/', views.cart, name='cart'),
    path('minus-cart/<int:id>', views.minus_cart, name='minus_cart'),
    path('plus-cart/<int:id>', views.plus_cart, name='plus_cart'),
]
