
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import date, timedelta
from pets.models import Pet
from .models import Vaccination, Vaccine
from .forms import VaccinationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

from django.utils import timezone
from dateutil.relativedelta import relativedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Регистрация шрифта с кириллицей (один раз при запуске)
pdfmetrics.registerFont( 
    TTFont('DejaVu', os.path.join(settings.BASE_DIR, 'DejaVuSans.ttf')))


@login_required
def vaccination_list(request):
    vaccinations = Vaccination.objects.filter(
      owner=request.user
    ).select_related('pet', 'vaccine').order_by('-date_given')
    return render(request, 'health/vaccination_list.html', {'vaccinations': vaccinations})

@login_required
def vaccination_upcoming(request):
    today = timezone.now().date()
    soon = today + timedelta(days=90)
    
    upcoming = Vaccination.objects.filter(
        owner=request.user,                    # ← ИСПРАВЛЕНО!
        next_due_date__gte=today,
        next_due_date__lte=soon
    ).select_related('pet', 'vaccine').order_by('next_due_date')

    overdue = Vaccination.objects.filter(
        owner=request.user,                    # ← ИСПРАВЛЕНО!
        next_due_date__lt=today
    ).select_related('pet', 'vaccine')

    return render(request, 'health/vaccination_upcoming.html', {
        'upcoming': upcoming,
        'overdue': overdue,
    })

# health/views.py
class VaccinationCreateView(LoginRequiredMixin, CreateView):
    model = Vaccination
    form_class = VaccinationForm
    template_name = 'health/vaccination_form.html'
    success_url = reverse_lazy('health:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user          # ← обязательно передаём
        return kwargs

    def form_valid(self, form):
        vaccination = form.save(commit=False)
        vaccination.owner = self.request.user
        vaccination.save()
        messages.success(self.request, f"Прививка для {vaccination.pet.name} добавлена!")
        return redirect(self.success_url)
    

@login_required
def vaccination_update(request, pk):
    vaccination = get_object_or_404(Vaccination, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = VaccinationForm(request.POST, instance=vaccination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Прививка обновлена')
            return redirect('vaccination_list')
    else:
        form = VaccinationForm(instance=vaccination)
    return render(request, 'health/vaccination_form.html', {
        'form': form,
        'pet': vaccination.pet,
        'title': 'Редактировать прививку'
    })

@login_required
def vaccination_delete(request, pk):
    vaccination = get_object_or_404(Vaccination, pk=pk, owner=request.user)
    pet = vaccination.pet
    if request.method == 'POST':
        vaccination.delete()
        messages.success(request, 'Прививка удалена')
        return redirect('vaccination_list')
    return render(request, 'health/vaccination_confirm_delete.html', {
        'vaccination': vaccination,
        'pet': pet
    })

@login_required
def pet_pdf_export(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*cm,
        bottomMargin=2*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    story = []

    # Стили с твоим шрифтом DejaVu
    styles = {
        'title': ParagraphStyle('title', fontName='DejaVu', fontSize=26, alignment=TA_CENTER,
                                spaceAfter=20, textColor=colors.HexColor('#2c3e50')),
        'name': ParagraphStyle('name', fontName='DejaVu', fontSize=22, alignment=TA_CENTER,
                               spaceAfter=30, textColor=colors.HexColor('#2c3e50')),
        'normal': ParagraphStyle('normal', fontName='DejaVu', fontSize=14, leading=20),
        'heading': ParagraphStyle('heading', fontName='DejaVu', fontSize=18, spaceAfter=15,
                                  textColor=colors.HexColor('#2c3e50')),
        'footer': ParagraphStyle('footer', fontName='DejaVu', fontSize=10, textColor=colors.grey,
                                 alignment=TA_CENTER),
    }

    # Заголовок и имя
    story.append(Paragraph("ВЕТЕРИНАРНАЯ КАРТА", styles['title']))
    story.append(Paragraph(pet.name, styles['name']))

    # Фото по центру
    if pet.photo and os.path.exists(pet.photo.path):
        img = Image(pet.photo.path, width=9*cm, height=9*cm)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 1*cm))

    # Информация о питомце
    birth = pet.birth_date.strftime("%d.%m.%Y") if pet.birth_date else "—"
    if pet.birth_date:
        delta = relativedelta(timezone.now().date(), pet.birth_date)
        age = f"{delta.years} г. {delta.months} мес." if delta.years else f"{delta.months} мес."
    else:
        age = "не указан"

    info = f"""
    <b>Вид:</b> {pet.species}  <b>Порода:</b> {pet.breed}  <b>Пол:</b> {pet.get_gender_display()}<br/>
    <b>Дата рождения:</b> {birth}  <b>Возраст:</b> {age}
    """
    story.append(Paragraph(info, styles['normal']))
    story.append(Spacer(1, 1.5*cm))

    # Прививки
    story.append(Paragraph("Прививки", styles['heading']))

    data = [["Вакцина", "Дата прививки", "Следующая", "Статус"]]
    for v in pet.vaccinations.all().order_by('-date_given'):
        status = "ПРОСРОЧЕНО!" if v.is_overdue() else "В порядке"
        next_d = v.next_due_date.strftime("%d.%m.%Y") if v.next_due_date else "—"
        data.append([v.vaccine.short_name, v.date_given.strftime("%d.%m.%Y"), next_d, status])

    if len(data) == 1:
        story.append(Paragraph("Прививок пока нет", styles['normal']))
    else:
        table = Table(data, colWidths=[6.5*cm, 4*cm, 4*cm, 4.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (-1,-1), 'DejaVu'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9fa')),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(table)

    # Футер
    story.append(Spacer(1, 2*cm))
    footer = f"Сформировано {timezone.now().strftime('%d.%m.%Y в %H:%M')} • VetLog — твой личный ветеринарный журнал"
    story.append(Paragraph(footer, styles['footer']))

    # Генерация PDF
    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pet.name}_медкарта.pdf"'
    return response