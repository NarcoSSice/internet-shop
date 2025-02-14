from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Customer, Category, SubCategory, Product, Order, OrderItem, Shipping

models_list = [Order, OrderItem, Shipping]
prepopulated_models = [Category, SubCategory]


class SlugsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


for model in models_list:
    admin.site.register(model)

for model in prepopulated_models:
    admin.site.register(model, SlugsAdmin)


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'subcategory', 'description', 'price', 'image')
    prepopulated_fields = {"slug": ["name"]}

    class Media:
        css = {
            'all': ('shop/css/admin.css', )
        }
        js = (
            'shop/js/jquery/jquery.min.js',
            'shop/js/AI_admin_scripts.js',
        )


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
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
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(Customer, CustomerAdmin)
