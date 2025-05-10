from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from .views import CategoryViewSet, TagViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, register, user_login, user_logout

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

    # Заказы
    path('create_order/', create_order, name='create_order'),
    path('orders/', orders, name='orders'),
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns += router.urls

urlpatterns += [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
