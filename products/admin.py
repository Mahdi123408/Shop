from django.contrib import admin

from .models import (
    ProductCategory,
    ProductMedia,
    Product,
    Cart
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'sub_category',
        'is_active',
        'created_at'
    )

    list_filter = (
        'is_active',
        'created_at'
    )

    search_fields = (
        'name',
        'description'
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_per_page = 30


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'type',
        'is_active',
        'created_at'
    )

    list_filter = (
        'type',
        'is_active'
    )

    search_fields = (
        'name',
        'slug'
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_per_page = 30


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'price',
        'discount',
        'count_inventory',
        'is_active',
        'deleted',
        'created_at'
    )

    list_filter = (
        'is_active',
        'deleted',
        'created_at'
    )

    search_fields = (
        'title',
        'description',
        'slug'
    )

    filter_horizontal = (
        'category',
        'media'
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    list_per_page = 30


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'is_down',
        'created_at'
    )

    list_filter = (
        'is_down',
        'created_at'
    )

    search_fields = (
        'user__username',
        'product__title'
    )

    list_per_page = 30
