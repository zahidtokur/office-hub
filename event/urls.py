from django.urls import path
from .views import Create, InvitedToList, CreatedList

urlpatterns = [
    path('new/', Create.as_view()),
    path('invited-to/', InvitedToList.as_view()),
    path('mine/', CreatedList.as_view())
]