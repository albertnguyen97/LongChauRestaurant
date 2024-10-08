from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import os
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return(super().get_queryset().filter(status=Post.Status.PUBLISHED))


def get_pdf_file_name(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return f'pdfs/{slugify(filename)}{file_extension}'


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts', default='')
    body = CKEditor5Field()
    pdf_file = models.FileField(upload_to=get_pdf_file_name, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])