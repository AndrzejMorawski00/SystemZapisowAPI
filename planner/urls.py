from django.urls import path
from . import views
app_name = 'planner'

urlpatterns = [
    path('plans/', views.UserPlanListCreateAPIView.as_view(), name='user-plan-list'),
    path('plans/<int:pk>/', views.RetriveUserPlanView.as_view(), name='user-plan'),
    path('plans/<int:pk>/update/',
         views.UpdateUserPlanAPIView.as_view(), name='edit-plan'),
    path('plans/<int:pk>/delete/',
         views.DeleteUserPlanAPIView.as_view(), name='delete-plan'),

    path('semester/', views.UserSemesterListCreateAPIView.as_view(),
         name='user-semester-list'),
    path('semester/<int:pk>/', views.RetriveUserSemesterAPIView.as_view(),
         name='user-semester'),
    path('semester/<int:pk>/update/',
         views.UpdateUserSemesterAPIView.as_view(), name='edit-semester'),
    path('semester/<int:pk>/delete/',
         views.DeleteUserSemesterAPIView.as_view(), name='delete-semester'),
    path('register/', views.UserRegisterAPIView.as_view(), name='register-user')
]
