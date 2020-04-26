from django.urls import path
from .views import (
    HomeView,
    ProductView,
    CheckoutView,
    OrderSummary,
    add_to_cart,
    remove_from_cart,
    remove_single_from_cart,
    PaymentView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('product/<slug>/', ProductView.as_view(), name='Product'),
    path('checkout/', CheckoutView.as_view(), name='Checkout'),
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('remove-single-from-cart/<slug>/', remove_single_from_cart, name="remove-single-from-cart"),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
]
