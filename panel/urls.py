from django.urls import path
from . import views

app_name = 'panel'


urlpatterns = [
    path('', views.panel_home_view, name='home-view'),
    # Fetching
    path('fetch-semesters/', views.fetch_semesters_view,
         name='fetch-semesters-view'),
    path('fetch-subject-metadata/', views.fetch_subject_metadata_view,
         name='fetch-subject-metadata-view'),
    # Metadata
    path('metadata-list/<str:datatype>/',
         views.metadata_list_view, name='metadata-list-view'),
    path('metadata-list/metadata-edit/<str:datatype>/<int:obj_pk>/',
         views.metadata_edit_view, name='metadata-edit-view'),

    # Subjects
    path('subject-list/<int:pk>/', views.subject_list_view,
         name='subject-list-view'),
    path('subject-list/edit/<int:obj_pk>',
         views.subject_edit_view, name='subject-edit-view'),

    # semsters

    path('semester-list/', views.semester_list_view, name='semester-list-view'),
    path('semester-list/edit-semester/<int:obj_pk>',
         views.handle_semester_view, name='edit-semester-view'),
    path('semester-list/add-semester/',
         views.handle_semester_view, name='add-semester-view')

]
