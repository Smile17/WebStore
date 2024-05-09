from django.contrib import admin
from .models import *


def register_model_admin(model):
    class ModelAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]

    admin.site.register(model, ModelAdmin)


register_model_admin(Cinema)
register_model_admin(Hall)
register_model_admin(Film)
register_model_admin(Session)
register_model_admin(Ticket)
