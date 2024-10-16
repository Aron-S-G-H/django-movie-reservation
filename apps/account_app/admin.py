from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("first_name", 'last_name', 'phone', 'email', 'last_login')
    list_filter = ("is_staff", "is_active", "is_superuser")
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {"fields": ("password",)}),
        ('Personal information',
         {"fields": (
             'first_name',
             'last_name',
             'phone',
             'email',
             'last_login',
             'date_joined'
         )}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "phone", "password1", "password2", "is_superuser", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("phone", "first_name", "last_name")
    ordering = ("-date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)
