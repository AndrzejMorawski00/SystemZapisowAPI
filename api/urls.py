from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index-view'),
    path('api/', views.api_view, name='api-view'),

    path('api/tags/', views.CourseTagListAPIView.as_view(), name='tags-list-view'),
    path('api/tags/<int:pk>/', views.CourseTagRetriveAPIView.as_view(), name='tag-view'),

    path('api/types/', views.CourseTypeListAPIView.as_view(), name='types-list-view'),
    path('api/types/<int:pk>/', views.CourseTypeRetriveAPIView.as_view(), name='type-view'),

    path('api/effects/', views.CourseEffectListAPIView.as_view(), name='effects-list-view'),
    path('api/effects/<int:pk>/', views.CourseEffectRetriveAPIView.as_view(), name='effect-view'),

    path('api/semesters/', views.SemesterListAPIView.as_view(), name='semesters-list-view'),
    path('api/semesters/<int:pk>/', views.SemesterRetriveAPIView.as_view(), name='semester-view'),

    path('api/courses/<int:semester_pk>/', views.CourseListAPIView.as_view(), name='course-list-view'),
    path('api/courses/<int:semester_pk>/<int:course_pk>/', views.CourseRetrieveAPIView.as_view(), name='course-list-view'),
]
