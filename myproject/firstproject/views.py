from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from .models import Product, Order, OrderItem, Category, Tag
from .forms import ProductForm, CategoryForm, TagForm
from rest_framework import viewsets
from .serializers import CategorySerializer, TagSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

# Temporary in-memory cart storage (for demonstration purposes)
cart_items = {}

# Helper function to check if a user is a superuser
def is_superuser(user):
    return user.is_superuser

# Publicly accessible views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

class ProductListView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'products'

# Views for registered users
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

@csrf_exempt
@login_required
def cart(request):
    if request.method == 'POST' and 'remove_product_id' in request.POST:
        remove_product_id = request.POST.get('remove_product_id')
        if remove_product_id in cart_items:
            del cart_items[remove_product_id]
        return redirect('cart')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        if product_id in cart_items:
            cart_items[product_id]['quantity'] += quantity
        else:
            cart_items[product_id] = {
                'name': product.name,
                'price': product.price,
                'quantity': quantity
            }

        return redirect('cart')

    return render(request, 'cart.html', {'cart_items': cart_items})

def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})


@login_required
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        delivery_address = request.POST.get('delivery_address')

        order = Order.objects.create(
            order_number=f"ORD-{Order.objects.count() + 1}",
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address
        )

        for product_id, item in cart_items.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                discount=0
            )

        cart_items.clear()
        return redirect('catalog')

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def api_docs(request):
    return render(request, 'api_docs.html')

def profile(request):
    return render(request, 'profile.html')

# Views for sellers
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('firstproject.add_product', raise_exception=True), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('catalog')

# Views for administrators
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('firstproject.change_product', raise_exception=True), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_product.html'
    success_url = reverse_lazy('catalog')

# Views for superusers
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_superuser, login_url='/login/', redirect_field_name=None), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('firstproject.view_category', raise_exception=True), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    success_url = reverse_lazy('category_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('firstproject.view_tag', raise_exception=True), name='dispatch')
class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'

class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'add_tag.html'
    success_url = reverse_lazy('tag_list')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer