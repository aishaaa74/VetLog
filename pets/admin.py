# pets/admin.py
from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'owner', 'get_age')  # ← изменил 'age' → 'get_age'
    list_filter = ('species', 'owner')
    search_fields = ('name', 'breed')

    # Добавляем метод, чтобы Django понял, что это возраст
    def get_age(self, obj):
        return obj.age()
    get_age.short_description = 'Возраст'  # название колонки в админке