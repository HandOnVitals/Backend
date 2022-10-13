from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from readings import views

urlpatterns = [
    path('readings/', views.Readings.as_view()),
    path('readings/<str:reading_id>', views.ReadingsObject.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
