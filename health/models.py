from django.db import models

# health/models.py
from django.db import models
from pets.models import Pet
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib.auth.models import User

class Vaccine(models.Model):
    name = models.CharField("Полное название вакцины", max_length=200)
    short_name = models.CharField("Короткое название", max_length=50, help_text="Например: DHPPi+L, Нобивак Rabies")
    for_species = models.CharField("Для каких животных", max_length=100, default="Собаки и кошки")
    revaccination_months = models.PositiveIntegerField("Ревакцинация через (месяцев)", default=12)

    def __str__(self):
        return f"{self.short_name} ({self.name})"

class Vaccination(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vaccinations')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT)
    date_given = models.DateField("Дата прививки")
    next_due_date = models.DateField("Следующая прививка", null=True, blank=True)
    clinic = models.CharField("Клиника", max_length=200, blank=True)
    notes = models.TextField("Заметки", blank=True)

    def save(self, *args, **kwargs):
        if self.vaccine and self.date_given and not self.next_due_date:
            self.next_due_date = self.date_given + relativedelta(months=self.vaccine.revaccination_months)
        super().save(*args, **kwargs)

    def is_overdue(self):
        if not self.next_due_date:
            return False
        return timezone.now().date() > self.next_due_date

    def __str__(self):
        return f"{self.vaccine.short_name} → {self.pet.name} ({self.date_given})"

    class Meta:
        ordering = ['-date_given']


class Treatment(models.Model):
    """Обработки от блох, клещей, глистов и т.д."""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='treatments')
    TREATMENT_TYPES = [
        ('flea', 'От блох/клещей'),
        ('deworm', 'Дегельминтизация'),
        ('tick', 'От клещей отдельно'),
        ('complex', 'Комплексная обработка'),
    ]
    treatment_type = models.CharField("Тип обработки", max_length=20, choices=TREATMENT_TYPES)
    drug = models.CharField("Препарат", max_length=200)
    date_given = models.DateField("Дата обработки")
    next_due_date = models.DateField("Следующая обработка", null=True, blank=True)
    notes = models.TextField("Заметки", blank=True)

    def __str__(self):
        return f"{self.get_treatment_type_display()} — {self.pet.name}"

    class Meta:
        ordering = ['-date_given']


class Visit(models.Model):
    """Посещения ветеринара"""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField("Дата визита")
    clinic = models.CharField("Клиника", max_length=200)
    reason = models.TextField("Причина обращения")
    diagnosis = models.TextField("Диагноз", blank=True)
    treatment = models.TextField("Назначенное лечение", blank=True)
    cost = models.DecimalField("Стоимость", max_digits=8, decimal_places=2, null=True, blank=True)
    documents = models.FileField("Чеки/анализы", upload_to='visits/', blank=True, null=True)

    def __str__(self):
        return f"Визит {self.pet.name} — {self.date}"

    class Meta:
        ordering = ['-date']