from django.contrib import admin
from .models import *
import admin_thumbnails
# Register your models here.
from django.contrib.admin import AdminSite
admin.site.site_header = 'Dancers for Life Administration'
admin.site.site_title = 'Dancers for Life Administration'


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

   
   

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')




admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ClassTicket, TicketAdmin)