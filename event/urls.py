from django.urls import path
from .views import *

urlpatterns = [
    path('new/', EventCreate.as_view()),
    path('<int:id>/update/', EventUpdate.as_view()),
    path('<int:event_id>/comments/', EventCommentList.as_view()),
    path('<int:event_id>/comments/new/', CommentCreate.as_view()),
    path('<int:event_id>/comments/<int:comment_id>/', CommentDetail.as_view()),
    path('<int:event_id>/comments/<int:comment_id>/delete/', CommentDelete.as_view()),
    path('<int:event_id>/invite/', InvitationCreate.as_view()),
    path('invitations/<int:invitation_id>/respond/', InvitationUpdate.as_view()),
    path('invitations/for-user/all/', InvitationList.as_view()),
    path('invitations/for-user/responded/', RespondedInvitationList.as_view()),
    path('invitations/for-user/pending/', PendingInvitationList.as_view()),
    path('user-invited/<int:user_id>/', InvitedEventsList.as_view()),
    path('user-created/<int:user_id>/', CreatedEventsList.as_view()),
]