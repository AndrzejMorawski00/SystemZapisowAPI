from django.forms import ModelForm

from .models import Course, Semester


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'recommended_for_first_year',
                  'type', 'ects', 'tags', 'effects']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].required = False
        self.fields['effects'].required = False


class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        fields = ['link', 'name', 'fetched']

    def __init__(self, *args, **kwargs):
        super(SemesterForm, self).__init__(*args, **kwargs)

        self.fields["link"].widget.attrs.update({
            'class': 'form__input',
        })

        self.fields["name"].widget.attrs.update({
            'class': 'form__input',
        })
        self.fields["fetched"].widget.attrs.update({
            'class': 'form__checkbox',
        })
