from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Distributor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


def validate_exp_greater_than_mfg(value):
    if value < models.F('mfg'):
        raise ValidationError(
            _("Ngày hết hạn phải sau ngày sản xuất. ")
        )


class Ingredient(models.Model):
    distributor = models.ForeignKey(Distributor,
                                    related_name='products',
                                    on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    quantity_product = models.PositiveIntegerField(default=0)
    returnable = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    address = models.CharField(max_length=100, default="Ha Noi")
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    mfg = models.DateField(blank=True, null=True, default='2023-04-04')
    exp = models.DateField(blank=True, null=True, default='2025-04-04')

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='dishes/%Y/%m/%d', blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    is_available = models.BooleanField(default=True)
    returnable = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=0, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    discounts_dish = models.ManyToManyField('Discount', related_name='dishes', blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant:display_menu_item', arg='self.id')


class Discount(models.Model):
    APPLY_OPTIONS = (
        ('CODE', 'Apply Code'),
        ('NO CODE', 'Apply Dish')
    )

    name = models.CharField(max_length=100)
    option = models.CharField(max_length=12, choices=APPLY_OPTIONS)
    code = models.CharField(max_length=20, blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateField()
    dishes_discount = models.ManyToManyField(Dish, related_name='discounts', blank=True)

    def __str__(self):
        return self.name
