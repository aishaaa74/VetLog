# pets/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Pet(models.Model):
    GENDER_CHOICES = [('M', 'Самец'), ('F', 'Самка')]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField("Кличка", max_length=100)
    species = models.CharField("Вид животного", max_length=50, default="Собака")
    breed = models.CharField("Порода", max_length=100, blank=True)
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    photo = models.ImageField("Фото питомца", upload_to='pets/', blank=True, null=True)
    weight = models.DecimalField("Текущий вес (кг)", max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def age(self):
        """Возвращает возраст питомца в человекочитаемом виде"""
        if not self.birth_date:
            return "Неизвестно"
        
        today = date.today()
        years = today.year - self.birth_date.year
        
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        
        if years >= 5:
            return f"{years} лет"
        elif years >= 1:
            return f"{years} год" if years == 1 else f"{years} года"
        else:
            months = (today.year - self.birth_date.year) * 12 + today.month - self.birth_date.month
            if today.day < self.birth_date.day:
                months -= 1
            return f"{months} мес." if months > 0 else "Меньше месяца"

    def __str__(self):
        return f"{self.name} ({self.species})"   # ← Теперь работает!

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"