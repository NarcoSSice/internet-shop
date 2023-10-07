from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Category, SubCategory, Product, Order, OrderItem, Shipping

models_list = [Order, OrderItem, Shipping]
prepopulated_models = [Product, Category, SubCategory]


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


for model in models_list:
    admin.site.register(model)

for model in prepopulated_models:
    admin.site.register(model, CategoriesAdmin)

admin.site.register(Customer, UserAdmin)
