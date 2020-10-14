from django.urls import include, path
from .views import Create, Update, UploadAvatar, List, CreateSkill, DeleteSkill
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('new/', Create.as_view()),
    path('login/', obtain_auth_token),
    path('all/', List.as_view()),
    path('<int:pk>/update/', Update.as_view()),
    path('<int:pk>/upload-avatar/', UploadAvatar.as_view()),
    path('<int:pk>/skills/new/', CreateSkill.as_view()),
    path('<int:pk>/skills/<int:s_pk>/delete/', DeleteSkill.as_view()),
]