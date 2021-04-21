from django.contrib import admin
from mainapp.models import ProductCategory, Product
# Register your models here.

admin.site.register(ProductCategory)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', 'short_description', ('price', 'quantity'), 'category', 'is_active')
    readonly_fields = ('short_description',)
    ordering = ('-name',)
    search_fields = ('name',)
