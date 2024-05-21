from django.contrib import admin
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils import timezone

from .models import Menu, Booking
# Register your models here.

admin.site.register(Menu)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'phone_number', 'guest_number', 'reservation_date', 'reservation_slot')
    actions = ['export_to_json']
    list_filter = ['first_name', 'phone_number', 'guest_number', 'reservation_date', 'reservation_slot']
    search_fields = ['first_name', 'phone_number', 'reservation_date', 'reservation_slot']
    ordering = ['first_name', 'reservation_date', 'reservation_slot']

    def export_to_json(self, request, queryset):
        data = serialize('json', queryset)
        filename = f"bookings_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    export_to_json.short_description = "Export selected bookings to JSON"


admin.site.register(Booking, BookingAdmin)

