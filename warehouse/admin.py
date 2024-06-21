from django.contrib import admin
from .models import Distributor, Category, Ingredient, Dish, Discount
from .resources import IngredientResource, DishResource, DiscountResource
from import_export.admin import ImportExportModelAdmin


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = IngredientResource
    list_display = ['name', 'distributor', 'quantity_product', 'price', 'available', 'mfg', 'exp']
    search_fields = ['name', 'distributor__name']
    list_filter = ['available', 'created', 'updated', 'distributor']
    ordering = ['name']
    date_hierarchy = 'created'


@admin.register(Dish)
class DishAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DishResource
    filter_horizontal = ['discounts_dish']
    list_display = ['name', 'category', 'price', 'is_available', 'returnable', 'total_ingredients']
    search_fields = ['name', 'category__name']
    list_filter = ['is_available', 'returnable', 'category', 'name']
    ordering = ['name']
    actions = ['add_discount_to_all_dishes']

    def total_ingredients(self, obj):
        return obj.ingredients.count()

    total_ingredients.short_description = 'Total Ingredients'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        if instance.discounts_dish.exists():
            discount = instance.discounts_dish.first()
            instance.discounted_price = instance.price - (instance.price * discount.discount_percent / 100)
        else:
            instance.discounted_price = None
        instance.save()


@admin.register(Discount)
class DiscountAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DiscountResource
    list_display = ['name', 'option', 'discount_percent', 'start_date', 'end_date', 'total_dishes']
    search_fields = ['name', 'code']
    list_filter = ['option', 'start_date', 'end_date']
    ordering = ['name']
    date_hierarchy = 'start_date'
    filter_horizontal = ['dishes_discount']

    def total_dishes(self, obj):
        return obj.dishes_discount.count()

    total_dishes.short_description = 'Total Dishes'

