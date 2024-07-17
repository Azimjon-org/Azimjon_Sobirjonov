from django.contrib import admin
from django.utils.html import format_html

from apps.models import Category, Product, User


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    search_fields = 'name',

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'price'
    autocomplete_fields = 'category',

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
    # list_display = ['name', 'img_display']
    #
    # @admin.display(description='Rasm')
    # def img_display(self, obj):
    #     photo = obj.image_set.order_by('-created_at').first()
    #     return format_html('<img src="{}" width="57" height="40" />', photo.image.url)
    #
