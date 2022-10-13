from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from pacients import views

urlpatterns = [
    path('pacients/<str:health_number>/readings/', views.Pacients.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)