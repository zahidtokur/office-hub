from django.urls import include, path
from .views import UserRegister, UserUpdate, UpdateAvatar, UserList, UserDetail, SkillCreate, SkillDelete
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('new/', UserRegister.as_view()),
    path('login/', obtain_auth_token),
    path('all/', UserList.as_view()),
    path('<int:id>/', UserDetail.as_view()),
    path('<int:pk>/update/', UserUpdate.as_view()),
    path('<int:pk>/upload-avatar/', UpdateAvatar.as_view()),
    path('<int:pk>/skills/new/', SkillCreate.as_view()),
    path('<int:pk>/skills/<int:s_pk>/delete/', SkillDelete.as_view()),
]