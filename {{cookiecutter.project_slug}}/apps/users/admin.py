from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"), 
            {
                "fields": (
                    "honorifics",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "suffix",
                    "email",
                    "employee_number",
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "full_name", "employee_number", "is_superuser"]
    search_fields = [
        "honorifics",
        "first_name",
        "middle_name",
        "last_name",
        "suffix",
        "email",
        "employee_number",
    ]

    @admin.display(description="Full Name")
    def full_name(self, obj) -> str:
        return obj.full_name
