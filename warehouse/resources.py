from import_export import resources
from .models import Ingredient, Dish, Discount


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        import_id_fields = ('id',)
        fields = (
        'id', 'distributor', 'name', 'slug', 'quantity_product', 'returnable', 'image', 'description', 'price',
        'address', 'available', 'created', 'updated', 'mfg', 'exp')


class DishResource(resources.ModelResource):
    class Meta:
        model = Dish
        import_id_fields = ('id',)
        fields = (
        'id', 'name', 'description', 'image', 'ingredients', 'is_available', 'returnable', 'price', 'category',
        'discounts_dish', 'discounted_price')


class DiscountResource(resources.ModelResource):
    class Meta:
        model = Discount
        import_id_fields = ('id',)
        fields = ('id', 'name', 'option', 'code', 'discount_percent', 'start_date', 'end_date', 'dishes_discount')
