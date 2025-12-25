# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pets.models import Pet
from health.models import Vaccination
from datetime import timedelta
from django.utils import timezone

@login_required
def dashboard(request):
    pets = Pet.objects.filter(owner=request.user)
    
    # Ближайшие прививки (за последние 30 дней и будущие 60 дней)
    today = timezone.now().date()
    soon = today + timedelta(days=60)
    overdue = Vaccination.objects.filter(
        pet__owner=request.user,
        next_due_date__lt=today
    )
    upcoming = Vaccination.objects.filter(
        pet__owner=request.user,
        next_due_date__gte=today,
        next_due_date__lte=soon
    ).order_by('next_due_date')

    context = {
        'pets': pets,
        'overdue_vaccinations': overdue,
        'upcoming_vaccinations': upcoming,
        'total_pets': pets.count(),
    }
    return render(request, 'core/dashboard.html', context)