from django.contrib import admin
from .models import OrderCart, OrderItemCart
from django.core import paginator
from django.utils.functional import cached_property
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse

from django.utils.safestring import mark_safe

# Idea referred from
# https://hakibenita.com/optimizing-the-django-admin-paginator
class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 999999


def order_detail(obj):
    url = reverse('order_cart:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    url = reverse('order_cart:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItemCart
    raw_id_fields = ['dish']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = (
        f'attachment; filename={opts.verbose_name}.csv'
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(OrderCart)
class OrderCartAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', 'stripe_id', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
    date_hierarchy = 'created'
    inlines = [OrderItemInline]
    paginator = CustomPaginator


@admin.register(OrderItemCart)
class OrderItemCartAdmin(admin.ModelAdmin):
    list_display = ['order', 'dish', 'price', 'quantity']
    list_filter = ['order', 'dish']
    search_fields = ['order__id', 'dish__name']
    raw_id_fields = ['order', 'dish']


paginator = CustomPaginator



