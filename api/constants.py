from api.utils import get_initial_semester_id

api_endpoints = [
    {
        'name': 'Tags',
        'url': 'api:tags-list-view',
        'additional_data': None,
        'list_path': 'api/tags/',
        'detailed_path': 'api/tags/<int:pk>/'
    },
    {
        'name': 'Types',
        'url': 'api:types-list-view',
        'additional_data': None,
        'list_path': 'api/types/',
        'detailed_path': 'api/types/<int:pk>/'
    },
    {
        'name': 'Effects',
        'url': 'api:effects-list-view',
        'additional_data': None,
        'list_path': 'api/effects/',
        'detailed_path': 'api/effects/<int:pk>/'
    },
    {
        'name': 'Semesters',
        'url': 'api:semesters-list-view',
        'additional_data': None,
        'list_path': 'api/semesters/',
        'detailed_path': 'api/semesters/<int:pk>/'
    },
    {
        'name': 'Courses',
        'url': 'api:course-list-view',
        'additional_data': get_initial_semester_id(),
        'list_path': 'api/courses/<int:semester_pk>/',
        'detailed_path': 'api/courses/<int:semester_pk>/<int:course_pk>/'
    }
]
