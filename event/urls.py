from django.urls import path
from .views import *

urlpatterns = [
    path('new/', Create.as_view()),
    path('<int:id>/update/', Update.as_view()),
    path('<int:event_id>/invite/', InvitationCreate.as_view()),
    path('invitations/<int:invitation_id>/respond/', InvitationUpdate.as_view()),
    path('invitations/for-user/all/', InvitationList.as_view()),
    path('invitations/for-user/responded/', RespondedInvitationList.as_view()),
    path('invitations/for-user/pending/', PendingInvitationList.as_view()),
    path('user-invited/<int:user_id>/', InvitedToList.as_view()),
    path('user-created/<int:user_id>/', CreatedList.as_view()),
]