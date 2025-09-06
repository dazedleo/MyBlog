from django.db import models
from django.utils.text import slugify

import uuid
from accounts.models import User


# Create your models here.

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.tag_name
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.category

class Post(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("published", "Published"),
        ("rejected", "Rejected")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="users_post", null=True)
    tags = models.ManyToManyField(Tag, related_name="tags_post", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="posts_category", null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True) #
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    bookmarked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"

    def save(self, *args, **kwargs):

        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "Untitled Post"

class Commment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts_comment")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

