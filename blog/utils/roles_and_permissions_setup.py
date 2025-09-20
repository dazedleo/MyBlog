# create_roles_permissions_dict.py

import os
import django
import re
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
django.setup()

from accounts.models import Roles, permissions

# Helper function to convert permission names to snake_case
def to_snake_case(text):
    text = re.sub(r"[’'/]", "", text)  # remove special characters
    text = re.sub(r"\s+", "_", text)   # replace spaces with underscores
    return text.lower()

# Define permissions per role
roles_permissions = {
    "Visitor": [
        "Read public blog posts",
        "Register/login",
    ],
    "Registered User": [
        "Read public blog posts",
        "Register/login",
        "Comment on posts",
        "Like/bookmark posts",
    ],
    "Author": [
        "Read public blog posts",
        "Register/login",
        "Comment on posts",
        "Like/bookmark posts",
        "Write posts",
        "Edit own posts",
        "Submit post for review",
    ],
    "Editor": [
        "Read public blog posts",
        "Register/login",
        "Comment on posts",
        "Like/bookmark posts",
        "Write posts",
        "Edit own posts",
        "Submit post for review",
        "Approve/publish posts",
        "Edit others’ posts",
        "Moderate comments",
    ],
    "Admin": [
        "Read public blog posts",
        "Register/login",
        "Comment on posts",
        "Like/bookmark posts",
        "Write posts",
        "Edit own posts",
        "Submit post for review",
        "Approve/publish posts",
        "Edit others’ posts",
        "Moderate comments",
        "Manage users",
        "Manage site settings",
    ]
}

# Create roles and permissions
for role_name, perm_list in roles_permissions.items():
    role_obj, _ = Roles.objects.get_or_create(role_name=role_name)
    
    for perm_name in perm_list:
        perm_obj, _ = permissions.objects.get_or_create(permission=perm_name)
        role_obj.permissions.add(perm_obj)

print("Roles and permissions have been created and assigned successfully!")
