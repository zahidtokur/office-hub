from django.urls import path
from .views import Create

urlpatterns = [
    path('new/', Create.as_view())
]