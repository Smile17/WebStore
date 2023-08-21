from django.contrib import admin
from .models import *


def register_model_admin(model):
    class ModelAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]

    admin.site.register(model, ModelAdmin)


register_model_admin(Category)
register_model_admin(Product)