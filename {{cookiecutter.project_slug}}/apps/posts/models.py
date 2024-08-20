from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.utils import timezone
from utils.base_models.fields import PublicImageField
from utils.base_models.models import BaseModelManager, AbstractAuditedModel
from auxiliaries.status_tags.post_tags.models import PostTag

import os

def image_upload(instance, filename):
    filename, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f"{slugify(instance.title)}_{timestamp}{ext}"

# Create your models here.
class Post(AbstractAuditedModel):
    title = models.CharField(
        max_length=240,
    )
    body = models.TextField(null=True, blank=True)
    thumbnail = PublicImageField(upload_to=image_upload, blank=True, null=True)
    published_date = models.DateTimeField(verbose_name="Published Date", default=timezone.now)
    is_published = models.BooleanField(default=False, verbose_name="Publish post", choices=((False, 'Save as draft'), (True, 'Publish Post')))
    tags = models.ManyToManyField(PostTag, related_name="posts")

    def __str__(self):
        return str(self.title)

    @property
    def is_drafted(self):
        return not self.is_published

    def get_absolute_url(self):
        return reverse(
            "posts:detail",
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            "posts:update",
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "posts:delete",
            kwargs={"pk": self.pk}
            )

    class Meta:
        ordering = ['-published_date', 'is_published']
        get_latest_by = 'published_date'

class ScholarshipPostManager(BaseModelManager):
    def get_queryset(self):
        return Post.objects.filter(qualification_set__isnull=False)

    def active_scholarships(self):
        pks = [post.pk for post in self.get_queryset() if post.qualification_set.is_open]
        if pks:
            return Post.objects.filter(pk__in=pks)
        return Post.objects.none()

    def closed_scholarships(self):
        pks = [post.pk for post in self.get_queryset() if post.qualification_set.is_closed]
        if pks:
            return Post.objects.filter(pk__in=pks)
        return Post.objects.none()

    def published_scholarships(self):
        pks = [post.pk for post in self.get_queryset() if post.is_published]
        if pks:
            return Post.objects.filter(pk__in=pks)
        return Post.objects.none()

    def drafted_scholarships(self):
        pks = [post.pk for post in self.get_queryset() if post.is_drafted]
        if pks:
            return Post.objects.filter(pk__in=pks)
        return Post.objects.none()

    @property
    def active_scholarships(self):
        pks = [post.pk for post in self.get_queryset() if post.qualification_set.is_open]
        if pks:
            return Post.objects.filter(pk__in=pks)
        return Post.objects.none()

class ScholarshipPost(Post):
    objects = ScholarshipPostManager()

    def get_absolute_url(self):
        return reverse(
            "posts:scholarship_filter:detail",
            kwargs={"pk": self.pk}
            )

    class Meta:
        proxy=True

class BlogPostManager(BaseModelManager):
    def get_queryset(self):
        return Post.objects.filter(qualification_set__isnull=True)

class BlogPost(Post):
    objects = BlogPostManager()
    class Meta:
        proxy=True

    def get_list_instruction_element(cls):
        return render_to_string("posts/instructions.html")
