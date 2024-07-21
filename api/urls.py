from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index-view'),
    path('api/', views.api_view, name='api-view'),
    path('api/tags/', views.CourseTagListAPIView.as_view(), name='tags-list-view'),
    path('api/types/', views.CourseTypeListAPIView.as_view(), name='types-list-view'),
    path('api/effects/', views.CourseEffectListAPIView.as_view(), name='effects-list-view'),
    path('api/semesters/', views.SemesterListAPIView.as_view(), name='semesters-list-view'),
    path('api/courses/<int:semester_id>/', views.CourseListAPIView.as_view(), name='course-list-view'),
]
