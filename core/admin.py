from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email")
    # fields = ("username", "email", "phone_number")
    fieldsets = (
        (None, {"fields": ("username", "email", "phone_number")}),
        (
            "Basic Info",
            {
                "fields": (
                    "profile_dp",
                    "gender",
                    "dob",
                )
            },
        ),
        (
            "Permission Info",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "password",
                )
            },
        ),
    )


# admin.site.register(User)
admin.site.register(User, CUserAdmin)
