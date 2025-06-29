from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Shows 3 empty image slots by default
    min_num = 3  # Minimum 3 additional images required
    max_num = 3  # Maximum 3 additional images allowed
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "No image"
    preview.allow_tags = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'display_categories', 'seller', 'status', 'created_at')
    list_filter = ('status', 'condition')  # Removed 'category' since it's M2M
    search_fields = ('title', 'description', 'seller__phone_number')
    inlines = [ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('seller', 'title', 'description')
        }),
        ('Pricing & Details', {
            'fields': ('price', 'condition', 'category', 'status')
        }),
        ('Location & Media', {
            'fields': ('location', 'main_image')
        }),
    )

    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])
    display_categories.short_description = 'Categories'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Number of Products'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'preview')
    readonly_fields = ('preview',)
    search_fields = ('product__title',)

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "No image"
    preview.allow_tags = True