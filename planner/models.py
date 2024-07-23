from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from panel.models import Course


class UserPlan(models.Model):
    class PlanTypes(models.TextChoices):
        ENG = 'engineer'
        BAC = 'bachelors'

   
    name = models.CharField(unique=True, max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=PlanTypes.choices, default='', max_length=20)

    def __str__(self):
        return f'{self.owner} {self.name}'


class UserSemester(models.Model):
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f'{self.owner} {self.plan} {self.name}'
