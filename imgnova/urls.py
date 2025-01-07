
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_image, name='analyze'),  # Ensure this path ends with a slash
]