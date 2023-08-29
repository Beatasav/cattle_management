from django.contrib import admin
from .models import Cattle, Herd, Field


class CattleAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'breed', 'birth_date', 'entry_date', 'end_date']
    ordering = ['name']


admin.site.register(Cattle)


class HerdAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'field', 'description', 'start_date', 'is_active', 'herd_leader']
    ordering = ['field']


admin.site.register(Herd)


class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'coordinates', 'field_size', 'size_unit', 'field_type', 'is_active',
                    'description']
    ordering = ['name']

admin.site.register(Field)

