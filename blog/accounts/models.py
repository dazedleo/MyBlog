from django.db import models
import uuid
# from accounts.models import Roles

# Create your models here.

class permissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "permissions"

    def __str__(self):
        return self.permission

class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(permissions)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.role_name

class User(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, related_name="user_role")    
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
