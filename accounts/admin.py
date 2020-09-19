from django.contrib import admin
from .models import Profile
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone','address', 'photo']



class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',)
        }),
    )
    model = User
    # inlines = [ProfileInline]

    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']

admin.site.register(User, CustomUserAdmin)
