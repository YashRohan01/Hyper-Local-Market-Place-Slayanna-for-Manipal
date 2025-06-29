# Create your views here.
# users/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import DetailView
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import LoginForm, UserRegistrationForm
from products.forms import ProductStatusForm
from products.models import Product
from messaging.models import Message
from wishlist.models import Wishlist
from django.db.models.functions import Random
from django.db.models import Count
from django.db.models import Q


def custom_logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    products = Product.objects.filter(status='available').order_by(Random())[:6]
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    category_counts = Product.objects.values('category__name').annotate(count=Count('id'))

    category_map = {item['category__name']: item['count'] for item in category_counts}
    return render(request, 'users/home.html', {'products': products,'unread_count':unread_count,'category_counts': category_map,})

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    """def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)"""

def custom_login_view(request):
    """if request.user.is_authenticated:
        return redirect('home')"""
    
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm(request=request)
    
    return render(request, 'users/login.html', {'form': form})

def user_profile_view(request):
    user = request.user
    listed_products = Product.objects.filter(seller = user).order_by('-created_at')
    context = {
        'listed_products': listed_products,
    }
    return render(request,'users/profile.html',context)

def update_product_status(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == "POST":
        form = ProductStatusForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
    return redirect('profile')


def search_results_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(status='available')

    if query:
        products = products.filter(
            Q(title__icontains=query) | 
            Q(category__name__icontains=query)
        ).distinct()

    return render(request, 'products/search_results.html', {
        'products': products,
        'query': query
    })

def category_products(request, category_name):
    products = Product.objects.filter(category__name__icontains=category_name, status="available").order_by(Random())
    context = {
        'products': products,
        'category_name': category_name,
    }
    return render(request, 'products/products_by_category.html', context)