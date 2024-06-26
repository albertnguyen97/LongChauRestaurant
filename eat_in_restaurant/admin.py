from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Table, Order, Queue


class TableAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'booked')
    list_editable = ('booked',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('selected_table',)
    search_fields = ('selected_table',)


class QueueAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'dish', 'is_cooked')
    search_fields = ('table_number', 'dish', 'is_cooked')
    list_editable = ('is_cooked',)
    ordering = ('created_at',)


# Register your models with the admin site
admin.site.register(Table, TableAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Queue, QueueAdmin)