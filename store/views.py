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

from django.conf import settings

from twilio.rest import Client
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import json
import requests


def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def tix(request):
    user = request.user
    cart_products = RegisteredEvents.objects.filter(user=user)

    # Display Total on Cart Page

    context = {
        'cart_products': cart_products,
        'amount': amount,
    }
    return render(request, 'store/cart.html', context)


def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:4]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
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
    item_already_in_cart = ClassTicket.objects.filter(product=product, user=user).exists()
    
    context = {
        'product': product,
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
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accnt/profile.html', {'addresses':addresses, 'orders':orders})


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


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')



@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')

def send_whatsapp_message(title, image, price, quantity, whatsapp, state):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC8377f54cdd5a489e9adee3de643a5317'
    auth_token = '4318df2431cda389629d25a494da0065'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+2349166059162',
            body = f"{whatsapp}, just placed an order for {quantity} {title}, {price}, from {state}",
            media_url=[image]
        )

@login_required
def checkout(request):
    user = request.user

    # Check if the user has at least one address
    if not Address.objects.filter(user=user).exists():
        return redirect('store:add-address')

    address_id = request.GET.get('address')

    address = get_object_or_404(Address, id=address_id)

    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)


    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        bb = Address.objects.filter(user=user).values()
        send_whatsapp_message(title=c.product.title, image=c.product.product_image.url, price=c.product.price, quantity=c.quantity, whatsapp= bb[0]['whatsapp'], state=bb[0]['state'],)
        c.delete()
    
    return redirect('store:orders')


@login_required
def orders(request):
    
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders': all_orders})








                       
                       


    return redirect('store:orders')


def shop(request):
    return render(request, 'store/shop.html')





def test(request):
    return render(request, 'store/test.html')
