# pets/views.py
from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pet
from .forms import PetForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image as RLImage, Spacer
from reportlab.lib import colors
from io import BytesIO
import os

@login_required
def pet_list(request):
    """Список питомцев пользователя"""
    pets = Pet.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'pets/pet_list.html', {'pets': pets})

@login_required
def pet_create(request):
    """Добавить нового питомца"""
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f'Питомец {pet.name} успешно добавлен!')
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'pets/pet_form.html', {'form': form, 'title': 'Добавить питомца'})

@login_required
def pet_detail(request, pk):
    """Карточка питомца"""
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    return render(request, 'pets/pet_detail.html', {'pet': pet})

@login_required
def pet_update(request, pk):
    """Редактировать питомца"""
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Информация о {pet.name} обновлена!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/pet_form.html', {
        'form': form, 
        'title': f'Редактировать {pet.name}'
    })

@login_required
def pet_delete(request, pk):
    """Удалить питомца"""
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'{pet_name} удалён из списка питомцев.')
        return redirect('pet_list')
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})


