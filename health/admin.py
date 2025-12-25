from django.contrib import admin
from .models import Treatment, Visit

# health/admin.py
from django.contrib import admin
from .models import Vaccine, Vaccination

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'revaccination_months')
    search_fields = ('short_name', 'name')

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('pet', 'vaccine', 'date_given', 'next_due_date', 'is_overdue')
    list_filter = ('vaccine', 'date_given')

    

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'treatment_type', 'drug', 'date_given', 'next_due_date')
    list_filter = ('treatment_type',)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'clinic', 'cost')
    list_filter = ('date',)