from django.shortcuts import render

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
