from django.urls import include, path
from .views import Create, Update, UploadAvatar, List
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('new/', Create.as_view()),
    path('login/', obtain_auth_token),
    path('all/', List.as_view()),
    path('<int:pk>/update/', Update.as_view()),
    path('<int:pk>/upload-avatar/', UploadAvatar.as_view()),
]