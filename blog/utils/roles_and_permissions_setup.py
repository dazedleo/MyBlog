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
    "visitor": [
        "read_public_blog_posts",
        "register_login",
    ],
    "registered_user": [
        "read_public_blog_posts",
        "register_login",
        "comment_on_posts",
        "like_bookmark_posts",
    ],
    "author": [
        "read_public_blog_posts",
        "register_login",
        "comment_on_posts",
        "like_bookmark_posts",
        "write_posts",
        "edit_own_posts",
        "submit_post_for_review",
    ],
    "editor": [
        "read_public_blog_posts",
        "register_login",
        "comment_on_posts",
        "like_bookmark_posts",
        "write_posts",
        "edit_own_posts",
        "submit_post_for_review",
        "approve_publish_posts",
        "edit_others_posts",
        "moderate_comments",
    ],
    "admin": [
        "read_public_blog_posts",
        "register_login",
        "comment_on_posts",
        "like_bookmark_posts",
        "write_posts",
        "edit_own_posts",
        "submit_post_for_review",
        "approve_publish_posts",
        "edit_others_posts",
        "moderate_comments",
        "manage_users",
        "manage_site_settings",
    ]
}

# Create roles and permissions
for role_name, perm_list in roles_permissions.items():
    role_obj, _ = Roles.objects.get_or_create(role_name=role_name)
    
    for perm_name in perm_list:
        perm_obj, _ = permissions.objects.get_or_create(permission=perm_name)
        role_obj.permissions.add(perm_obj)

print("Roles and permissions have been created and assigned successfully!")
