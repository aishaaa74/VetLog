from django.urls import path
from . import views

app_name = 'health'          

urlpatterns = [
    path('', views.vaccination_list, name='list'),
    path('create/', views.VaccinationCreateView.as_view(), name='create'),          
    path('upcoming/', views.vaccination_upcoming, name='upcoming'),
    path('<int:pk>/update/', views.vaccination_update, name='update'),
    path('<int:pk>/delete/', views.vaccination_delete, name='delete'),
    path('pet/<int:pet_id>/pdf/', views.pet_pdf_export, name='pet_pdf'),
]