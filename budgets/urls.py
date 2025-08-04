from django.urls import path
from . import views

urlpatterns = [
    path('budgets/', views.budgets, name='budgets')
]