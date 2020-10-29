from django.urls import path
from .views import FeedbackList, FeedbackListCategory, FeedbackCreate, FeedbackDelete, UserFeedbackList

urlpatterns = [
    path('all/', FeedbackList.as_view()),
    path('category/<str:category>/', FeedbackListCategory.as_view()),
    path('new/', FeedbackCreate.as_view()),
    path('by-user/<int:user_id>/', UserFeedbackList.as_view()),
    path('delete/<int:feedback_id>/', FeedbackDelete.as_view()),
]