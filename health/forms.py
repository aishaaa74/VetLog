# health/forms.py
from django import forms

from pets.models import Pet
from .models import Vaccination


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['pet', 'vaccine', 'date_given', 'next_due_date', 'clinic', 'notes']
        widgets = {
            'date_given': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительная информация...'}),
        }

    def __init__(self, *args, **kwargs):
        # ← ВОТ САМАЯ ВАЖНАЯ СТРОКА — user может быть None!
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            self.fields['pet'].queryset = user.pets.all()
        else:
            self.fields['pet'].queryset = Pet.objects.none()  # пусто, если нет юзера
            
        self.fields['vaccine'].empty_label = "— Выберите вакцину —"