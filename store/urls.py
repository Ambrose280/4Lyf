from store.forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'store'


urlpatterns = [
    path('', views.home, name="home"),
    # URL for Cart and Checkout
    path('classes/', views.tix, name="classes"),

    #URL for Products
    path('lesson/<slug:slug>/', views.detail, name="product-detail"),
    path('categories/', views.all_categories, name="all-categories"),
    path('<slug:slug>/', views.category_products, name="category-products"),

    path('shop/', views.shop, name="shop"),

 
    path('user/profile/', views.profile, name="profile"),
    path('user/add-address/', views.AddressView.as_view(), name="add-address"),
    path('user/remove-address/<int:id>/', views.remove_address, name="remove-address"),
    path('product/test/', views.test, name="test"),


    
]
