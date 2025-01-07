
from django.urls import path
from imgnova import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_image, name='analyze'),
]

