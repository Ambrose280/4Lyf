import django
from django.contrib.auth.models import User
from store.models import *
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import subprocess
import os
from django.conf import settings
import stripe
from twilio.rest import Client
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import json
import requests


def custom_404(request, exception):
    return render(request, '404.html', status=404)



@login_required
def register(request):
    user = request.user
    product_id = request.POST['prod_id']
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = ClassTicket.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        return render(request, 'store/cart.html')
    else:
        stripe.api_key = ''
        ClassTicket.objects.create(user=user, product=product).save()

        pay = stripe.checkout.Session.create(success_url="https://dancersforlife.vercel.app/classes",line_items=[{"price": "price_1OP8xRE1PS5aYBreXABY5wP8", "quantity": 1}],mode="payment",)
        oo = pay['url']
        return redirect(oo)

# ndbox.paypal.com

@login_required
def tix(request):
    user = request.user
    cart_products = ClassTicket.objects.filter(user=user)

    # Display Total on Cart Page

    context = {
        'cart_products': cart_products,
    }
    return render(request, 'store/cart.html', context)


def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:4]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    events = Event.objects.all().values()
    context = {
        'categories': categories,
        'events':events,
        'products': products,
    }
    return render(request, 'store/index.html', context)

from django.contrib.auth.decorators import login_required

@login_required
def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Assuming you have a 'user' variable available (e.g., through request.user)
    user = request.user
    
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    item_already_in_cart = ClassTicket.objects.filter(product=product, user=request.user.id).exists()
    paypal_client_id = os.getenv("PAYPAL_CLIENT_ID")
    context = {
        'product': product,
        'paypal_client_id':paypal_client_id,
        'related_products': related_products,
        'item_already_in_cart': item_already_in_cart,
    }
    return render(request, 'store/detail.html', context)



def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})



def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    
    # Paginate the products
    page = request.GET.get('page')
    paginator = Paginator(products, 3)  # You can change the number of products per page (e.g., 12)
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)

# {% with products_length=products|length %}
#   The length of my_list is {{ products_length }}.
# {% endwith %}


# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    
    return render(request, 'accnt/profile.html', {'addresses':addresses,})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'accnt/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            whatsapp = form.cleaned_data['whatsapp'],
            state = form.cleaned_data['state'],
            reg = Address(user=user, whatsapp=whatsapp, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')




    return redirect('store:orders')


def shop(request):
    return render(request, 'store/shop.html')





def test(request):
    return render(request, 'store/test.html')
