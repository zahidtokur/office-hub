from django.urls import path
from .views import *

urlpatterns = [
    path('new/', EventCreate.as_view()),
    path('<int:id>/update/', EventUpdate.as_view()),
    path('<int:id>/delete/', EventDelete.as_view()),
    path('<int:event_id>/comments/', EventCommentList.as_view()),
    path('<int:event_id>/comments/new/', CommentCreate.as_view()),
    path('<int:event_id>/comments/<int:comment_id>/', CommentDetail.as_view()),
    path('<int:event_id>/comments/<int:comment_id>/delete/', CommentDelete.as_view()),
    path('<int:event_id>/invite/', InvitationCreate.as_view()),
    path('invitations/<int:invitation_id>/update/', InvitationUpdate.as_view()),
    path('invitations/by-user/<int:user_id>/all/', InvitationList.as_view()),
    path('invitations/by-user/<int:user_id>/responded/', RespondedInvitationList.as_view()),
    path('invitations/by-user/<int:user_id>/pending/', PendingInvitationList.as_view()),
    path('by-user/<int:user_id>/invited-to/', InvitedEventsList.as_view()),
    path('by-user/<int:user_id>/created/', CreatedEventsList.as_view()),
]