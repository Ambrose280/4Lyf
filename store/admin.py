from django.contrib import admin
from .models import Address, Category, Product, Cart, Order
import admin_thumbnails
# Register your models here.
from django.contrib.admin import AdminSite
admin.site.site_header = 'Goody Footwears Administration'
admin.site.site_title = 'Goody Footwears Administration'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'whatsapp')
    list_filter = ('whatsapp', 'state')
    list_per_page = 10
    search_fields = ('whatsapp', 'state')


@admin_thumbnails.thumbnail('category_image')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image_thumbnail', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 100
    search_fields = ('title', 'description')

 
@admin_thumbnails.thumbnail('product_image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'product_image_thumbnail', 'is_active', 'is_featured', 'updated_at')
    list_editable =  ('category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')

    actions = ['create_eight_products']

   
   

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 200
    search_fields = ('user', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 200
    search_fields = ('user', 'product')


admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)