from django.contrib import admin
from .models import Profile
from django.core import paginator
from django.utils.functional import cached_property


# Idea referred from
# https://hakibenita.com/optimizing-the-django-admin-paginator
class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 10000


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    paginator = CustomPaginator
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']