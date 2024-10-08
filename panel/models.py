from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from panel.utils import unique_slugify

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    recommended_for_first_year = models.BooleanField(default=False)
    type = models.ForeignKey(
        'CourseType', on_delete=models.SET_NULL, null=True)
    ects = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    tags = models.ManyToManyField('CourseTag', blank=True)
    effects = models.ManyToManyField('CourseEffect', blank=True)

    def __str__(self):
        return f'{self.semester.name} {self.name}'


class CourseEffect(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pk} {self.name}'


class CourseTag(models.Model):
    name = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=100, default='')

    def save(self, *args, **kwargs):
        shortcut_letters = [s[0].capitalize() if len(s) > 1 else s[0]
                            for s in self.name.split(' ')]
        shortcut = ''.join(shortcut_letters)
        self.shortcut = shortcut
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk} {self.name}'


class CourseType(models.Model):
    name = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10, default='')

    def __str__(self):
        return f'{self.pk} {self.name}'


class Semester(models.Model):
    link = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    fetched = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        slug_str = f'{self.link}'.replace('/', '-')
        unique_slugify(self, slug_str)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class InvalidData(models.Model):
    value = models.TextField(default='')
