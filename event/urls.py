from django.urls import path
from .views import Create, InvitedToList, CreatedList

urlpatterns = [
    path('new/', Create.as_view()),
    path('user-invited/<int:user_id>/', InvitedToList.as_view()),
    path('user-created/<int:user_id>/', CreatedList.as_view()),
]