from django.urls import path
from .views import *

urlpatterns = [
    # Основные страницы
    path('', home, name='home'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('about/', about, name='about'),
    path('cart/', cart, name='cart'),
    path('profile/', profile, name='profile'),
    path('api/', api_docs, name='api_docs'),

    # Товары 
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),

    # Категории и теги
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='add_category'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tag/add/', TagCreateView.as_view(), name='add_tag'),
]
