# pets/forms.py
from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'gender', 'birth_date', 'photo', 'weight']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кличка питомца'}),
            'species': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Собака', 'Собака'),
                ('Кошка', 'Кошка'),
                ('Хомяк', 'Хомяк'),
                ('Птица', 'Птица'),
                ('Другое', 'Другое'),
            ]),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Порода (необязательно)'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Вес в кг'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Кличка',
            'species': 'Вид животного',
            'breed': 'Порода',
            'gender': 'Пол',
            'birth_date': 'Дата рождения',
            'photo': 'Фото питомца',
            'weight': 'Вес (кг)',
        }