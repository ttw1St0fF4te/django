from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('api/', views.api_docs, name='api_docs'),
    path('profile/', views.profile, name='profile'),
]
