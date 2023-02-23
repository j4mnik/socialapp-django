from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


class UserAdmin(UserAdmin):
    model = User
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "gender",
        "profile_picture",
        "date_of_birth",
        "created_at",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        ("Additional personal info", {"fields": ("gender", "profile_picture", "date_of_birth")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("first_name", "last_name", "date_of_birth", "profile_picture", "gender")}),)


admin.site.register(User, UserAdmin)
