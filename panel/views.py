import json
from django.db import models, IntegrityError
from django.db.models import Q
from django.contrib import messages
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from typing import Any, Dict, List, Literal, Optional, Type,  cast

from panel.types import CourseDataDict
from panel.utils import has_permission, schema

from .site_crawler import SiteCrawler
from .forms import CourseForm, SemesterForm
from .decoratos import user_authenticated
from .models import Semester, CourseEffect, CourseTag, CourseType, Course


@user_authenticated
def panel_home_view(request: HttpRequest):
    return render(request, 'panel/home_view.html', {'is_home': True})


@user_authenticated
def fetch_semesters_view(request: HttpRequest):
    sc = SiteCrawler('https://zapisy.ii.uni.wroc.pl')
    counter = 0
    if not has_permission(request, ['mod']):
        messages.error(
            request, "You don't have permission to perform this action")
        return redirect('panel:home-view')
    for link, name in sc.get_semesters():
        link, name = link.strip(), name.strip()
        try:
            Semester.objects.get(link=link)
        except Semester.DoesNotExist:
            Semester.objects.create(link=link, name=name)
            counter += 1
        except Semester.MultipleObjectsReturned:
            print(link, name)
            continue
    if counter == 0:
        messages.success(request, "Didn't fetch any semesters")
    elif counter == 1:
        messages.success(request, 'Fetched 1 semester')
    else:
        messages.success(request, f'Fetched {counter} semesters')
    return redirect('panel:home-view')


@user_authenticated
def fetch_subject_metadata_view(request: HttpRequest):
    if not has_permission(request, ['mod']):
        messages.error(
            request, "You don't have permission to perform this action")
        return redirect('panel:home-view')
    sc = SiteCrawler('https://zapisy.ii.uni.wroc.pl')
    metadata_dict = {'allEffects': CourseEffect,
                     'allTags': CourseTag, 'allTypes': CourseType}
    response = sc.get_metadata(list(metadata_dict.keys()))
    counter = 0
    for category, values in response.items():
        for id, name in values.items():
            if id.isnumeric():
                model = cast(Type[models.Model], metadata_dict[category])
                try:
                    model.objects.get(pk=int(id))
                except model.DoesNotExist:
                    model.objects.create(pk=int(id), name=name.strip())
                    counter += 1
                except model.MultipleObjectsReturned:
                    print(int(id), name.strip())
    if counter == 0:
        messages.success(request, "Didn't fetch any object")
    elif counter == 1:
        messages.success(request, 'Fetched 1 object')
    else:
        messages.success(request, f'Fetched {counter} objects')
    return redirect('panel:home-view')


@user_authenticated
def semester_list_view(request: HttpRequest):
    if request.method == 'POST':
        counter = 0
        checked_semesters = request.POST.getlist('semester_checked') or []
        tags = list(CourseTag.objects.all())
        effects = list(CourseEffect.objects.all())
        types = list(CourseType.objects.all())

        if not (tags and effects and types):
            messages.error(request, 'You need to fetch Metadata First')
            return redirect('panel:semester-list-view')

        selected_semesters: List[Semester] = []
        selected_semesters: List[Semester] = list(Semester.objects.filter(
            pk__in=[int(s) for s in checked_semesters if s.isnumeric()]))
        sc = SiteCrawler('https://zapisy.ii.uni.wroc.pl')
        for semester in selected_semesters:
            if semester.fetched:
                continue
            response = sc.get_semester_subjects(semester.link)
            for subject in response:
                is_valid = True
                subject_keys = ['id', 'name', 'courseType',
                                'recommendedForFirstYear', 'effects', 'tags', 'url']
                subject_dict = {}
                for key in list(subject_keys):
                    if key in subject:
                        subject_dict[key] = subject[key]
                    else:
                        is_valid = False
                ects = sc.get_subject_details(subject['url'])
                if is_valid:
                    tags: List[CourseTag] = []
                    course_type: Optional[CourseType] = None
                    effects: List[CourseEffect] = []
                    try:
                        tags = list(
                            CourseTag.objects.filter(pk__in=subject_dict['tags']))
                        course_type = CourseType.objects.get(
                            pk=subject_dict['courseType'])
                        effects = list(CourseEffect.objects.filter(
                            pk__in=subject_dict['effects']))
                        course = Course.objects.create(pk=int(
                            subject_dict['id']), name=subject_dict['name'], url=subject_dict['url'], semester=semester, recommended_for_first_year=subject_dict['recommendedForFirstYear'], ects=ects, type=course_type)
                        if tags:
                            course.tags.add(*tags)
                        if effects:
                            course.effects.add(*effects)
                        course.save()
                        counter += 1
                    except (CourseTag.DoesNotExist, CourseType.DoesNotExist, CourseEffect.DoesNotExist, Course.MultipleObjectsReturned, IntegrityError) as e:
                        print(f'Exception {e}')
                        continue
            semester.fetched = True
            semester.save()
        if counter == 0:
            messages.success(request, "Didn't fetch any subject")
        elif counter == 1:
            messages.success(request, 'Fetched 1 subject')
        else:
            messages.success(request, f'Fetched {counter} subjects')
    semester_list = Semester.objects.all()
    invalid_semesters = Course.objects.filter(type=None)
    for s in invalid_semesters:
        print(f'Invalid Semester: {s.pk}, {s.name}')
    return render(request, 'panel/semester_list_view.html', {'semester_list': semester_list, 'column_names': ['Semester', 'Fetched?', 'Select semesters to fetch data', 'View Subjects']})


@user_authenticated
def subject_list_view(request: HttpRequest, pk: int):
    MAX_PAGE_SIZE = 8
    filter_value = request.POST.get('search_value') or ''
    page_number = request.GET.get('page') or 1

    try:
        semester = Semester.objects.get(pk=pk)
        data = Course.objects.filter(semester=semester.pk)
        data = data.filter(name__contains=filter_value).order_by(
            'name') if filter_value else data.order_by('name')
        paginator = Paginator(data, MAX_PAGE_SIZE)
        page_obj = paginator.get_page(page_number)
        return render(request, 'panel/subject_list_view.html', {'page_obj': page_obj})
    except Semester.DoesNotExist:
        messages.error(request, "Semester with this id doesn't exist")
        return redirect('semester-list-view')


@user_authenticated
def add_subject_list(request: HttpRequest):
    if request.method == 'POST':
        data: str = request.POST.get('courses', '{}')
        counter = 0
        try:
            JSONData: CourseDataDict = json.loads(data)
            courses = JSONData['courses']
            semester = Semester.objects.get(pk=JSONData['semester'])

            for course in courses:
                type = CourseType.objects.get(pk=course['type']['id'])
                tags = CourseTag.objects.filter(
                    pk__in=[data['id'] for data in course['tags'] or []])
                effects = CourseEffect.objects.filter(
                    pk__in=[data['id'] for data in course['effects'] or []])
                try:
                    course_obj = Course.objects.create(pk=course['id'], name=course['name'], type=type,  url=course['url'],
                                                       semester=semester, recommended_for_first_year=course['recommended_for_first_year'], ects=course['ects'])
                    course_obj.tags.add(*tags)
                    course_obj.effects.add(*effects)
                    course_obj.save()
                    counter += 1
                except IntegrityError as e:
                    print(f"Integrity error for course {course['name']}: {e}")
        except (Semester.DoesNotExist, CourseType.DoesNotExist, json.JSONDecodeError) as e:
            print(e)
        if counter == 0:
            messages.success(request, "Didn't add any subject")
        elif counter == 1:
            messages.success(request, 'Added 1 subject')
        else:
            messages.success(request, f'Added {counter} subjects')

    return render(request, 'panel/add_subject_list.html', {'schema': schema})


@user_authenticated
def metadata_list_view(request: HttpRequest, datatype: Literal['tag', 'effect', 'type']):
    MAX_PAGE_SIZE = 8
    datatype_dict: Dict[str, Dict[str, Any]] = {
        'tag': {
            'name': 'Tags',
            'model': CourseTag,
        },
        'effect': {
            'name': 'Effects',
            'model': CourseEffect,
        },
        'type': {
            'name': 'Types',
            'model': CourseType,
        },
    }
    filter_value = request.POST.get('search_value') or ''
    page_number = request.GET.get("page") or 1
    edit = has_permission(request, ['mod'])
    if datatype in datatype_dict:
        model: models.Model = datatype_dict[datatype]['model']
        name: str = datatype_dict[datatype]['name']
        data = model.objects.filter(
            name__contains=filter_value).order_by('name') if filter_value else model.objects.all().order_by('name')
        paginator = Paginator(data, MAX_PAGE_SIZE)
        page_obj = paginator.get_page(page_number)
        return render(request, 'panel/metadata_list_view.html', {'page_obj': page_obj, 'name': name, 'datatype': datatype, 'edit': edit})
    else:
        return redirect('panel:home-view')


@user_authenticated
def metadata_edit_view(request: HttpRequest, datatype: Literal['tag', 'effect', 'type'], obj_pk: int):
    datatype_dict: Dict[str, Dict[str, Any]] = {
        'tag': {
            'name': 'Tag',
            'model': CourseTag,
        },
        'effect': {
            'name': 'Effect',
            'model': CourseEffect,
        },
        'type': {
            'name': 'Type',
            'model': CourseType,
        },
    }
    model = cast(Type[models.Model], datatype_dict[datatype]['model'])

    try:
        obj = model.objects.get(pk=obj_pk)
    except model.DoesNotExist:
        print(f"{datatype} object with key {obj_pk} doesn't exist")
        return redirect('panel:metadata-list-view', datatype=datatype)

    if request.method == 'POST':
        obj_name = request.POST.get('obj_name') or ''
        if obj_name:
            setattr(obj, 'name', obj_name)
            obj.save()
            messages.success(
                request, f'{datatype_dict[datatype]['name']} saved succesfully')
        else:
            messages.error(request, f'Failed to save{
                           datatype_dict[datatype]['name']}')
        return redirect('panel:metadata-list-view', datatype=datatype)
    else:
        name = datatype_dict[datatype]['name']
        return render(request, 'panel/metadata_edit_view.html', {'model': obj, 'name': name, 'datatype': datatype})


@user_authenticated
def subject_edit_view(request: HttpRequest, obj_pk: int):
    try:
        course = Course.objects.get(pk=obj_pk)
        semester_id = course.semester.pk
        if request.method == 'POST':
            course_form = CourseForm(request.POST, instance=course)
            if course_form.is_valid():
                course_form.save()
                messages.success(request, 'Changes saved')
                return redirect('panel:semester-list-view')
            else:
                messages.error(request, 'Something went wrong')
                return render(request, 'panel/subject_edit_view.html', {'course_form': course_form, 'semester_id': semester_id})
        else:
            course_form = CourseForm(instance=course)
            return render(request, 'panel/subject_edit_view.html', {'course_form': course_form, 'semester_id': semester_id})
    except Course.DoesNotExist:

        messages.error(request, "Course with this id doesn't exist")
        return redirect('panel:semester-list-view')


@user_authenticated
def handle_semester_view(request: HttpRequest,  obj_pk: Optional[int] = None):
    if request.method == "POST":
        if obj_pk:
            try:
                semester = Semester.objects.get(pk=obj_pk)
                semester_form = SemesterForm(request.POST, instance=semester)
            except Semester.DoesNotExist:
                messages.error(request, "Semester with this id doesn't exist")
                return redirect('panel:semester-list-view')
        else:
            semester_form = SemesterForm(request.POST)

        if semester_form.is_valid():
            messages.success(request, "Changes saved")
            semester_form.save()
        else:
            messages.error(request, "Something went wrong")
            return render(request, 'panel/handle_semester_view.html', {'semester_form': semester_form, 'action': 'Edit' if obj_pk else 'Add'})
        return redirect('panel:semester-list-view')

    else:
        if obj_pk:
            try:
                semester = Semester.objects.get(pk=obj_pk)
                semester_form = SemesterForm(instance=semester)
            except Semester.DoesNotExist:
                redirect('panel:semester-list-view')
        else:
            semester_form = SemesterForm()

        return render(request, 'panel/handle_semester_view.html', {'semester_form': semester_form, 'action': 'Edit' if obj_pk else 'Add'})
