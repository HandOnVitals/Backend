from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from readings import views

urlpatterns = [
    path('readings/', views.ReadingList.as_view()),
    path('readings/<int:pk>/', views.ReadingDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)