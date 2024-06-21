from django.contrib import admin
from .models import Post
from django.core.paginator import Paginator
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms


# Custom paginator with a fixed count of 50
class CustomPaginator(Paginator):
    def _get_count(self):
        return 50


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': CKEditor5Widget(),  # Use CKEditorWidget for the body field
        }

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)
