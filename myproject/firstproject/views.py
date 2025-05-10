from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from .models import Product, Order, OrderItem, Category, Tag
from .forms import ProductForm, CategoryForm, TagForm

# Temporary in-memory cart storage (for demonstration purposes)
cart_items = {}

def home(request):
    return render(request, 'home.html')

def catalog(request):
    return render(request, 'catalog.html')

def product_detail(request, product_id):
    return render(request, 'product_detail.html', {'product_id': product_id})

def add_product(request):
    return render(request, 'add_product.html')

def edit_product(request, product_id):
    return render(request, 'edit_product.html', {'product_id': product_id})

@csrf_exempt
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

def about(request):
    return render(request, 'about.html')

def api_docs(request):
    return render(request, 'api_docs.html')

def profile(request):
    return render(request, 'profile.html')

class ProductListView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('catalog')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_product.html'
    success_url = reverse_lazy('catalog')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog')

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    success_url = reverse_lazy('category_list')

class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'

class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'add_tag.html'
    success_url = reverse_lazy('tag_list')