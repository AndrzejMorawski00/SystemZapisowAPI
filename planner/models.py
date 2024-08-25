from django.db import models
from django.contrib.auth.models import User
from panel.models import Course
from panel.utils import unique_slugify

# Create your models here.

class PlanTypes(models.TextChoices):
    ENG = 'Inżynierskie'
    BAC = 'Licencjackie'


class UserPlan(models.Model):

    name = models.CharField(unique=True, null=False, max_length=100)
    slug = models.SlugField(unique=True, null=False,
                            default='',  max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=PlanTypes.choices,
                            default='', max_length=20)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner} {self.name}'


class UserSemester(models.Model):
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f'{self.owner} {self.plan} {self.name}'
