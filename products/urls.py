from django.urls import path
from products.views import (
        AddToCartView,
        CartView,
        CategoryView,
        CheckoutView,
        ClearCartView,
        OneCategoryView,
        ProductsView,
        RemoveCartItemView,
        UpdateCartItemView,
)

urlpatterns = [
        path('categories/', CategoryView.as_view() , name='categories'),
        path('categories/<str:slug>/', OneCategoryView.as_view() , name='categories'),
        path('products/', ProductsView.as_view(), name='products'),
        path('cart/', CartView.as_view(), name='cart'),
        path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='cart_add'),
        path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='cart_update'),
        path('cart/remove/<int:item_id>/', RemoveCartItemView.as_view(), name='cart_remove'),
        path('cart/clear/', ClearCartView.as_view(), name='cart_clear'),
        path('cart/checkout/', CheckoutView.as_view(), name='cart_checkout'),

]
