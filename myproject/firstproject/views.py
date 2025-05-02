from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *


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

def cart(request):
    return render(request, 'cart.html')

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