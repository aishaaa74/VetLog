
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('add/', views.pet_create, name='pet_create'),
    path('<int:pk>/', views.pet_detail, name='pet_detail'),
    path('<int:pk>/update/', views.pet_update, name='pet_update'),
    path('<int:pk>/delete/', views.pet_delete, name='pet_delete'),
]