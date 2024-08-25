import re
from typing import List
from django.contrib.auth.models import User
from planner.models import PlanTypes, UserPlan, UserSemester


def create_user_semesters(plan_type: str, plan_pk: int, user: User) -> bool:
    duration = 0
    try:
        plan = UserPlan.objects.get(pk=plan_pk)
    except UserPlan.DoesNotExist:
        return False

    if plan_type == PlanTypes.BAC:
        duration = 6
    elif plan_type == PlanTypes.ENG:
        duration = 7
    try:
        for i in range(duration):
            semester_name = f'Semestr {i + 1}'
            UserSemester.objects.create(
                name=semester_name, owner=user, plan=plan)
        UserSemester.objects.create(name='Dzienanka 1', owner=user, plan=plan)
        UserSemester.objects.create(name='Dziekanka 2', owner=user, plan=plan)
    except (UserSemester.DoesNotExist, UserSemester.MultipleObjectsReturned):
        UserSemester.objects.filter(owner=user, plan=plan).delete()
        return False

    return True


def validate_username(username: str) -> List[str]:
    error_messages: List[str] = []
    if len(username) <= 5:
        print('Username', len(username))
        error_messages.append(
            "Nazwa użytkownika musi mieć więcej niż 5 znaków.")
    users = User.objects.filter(username=username)
    if len(list(users)):
        error_messages.append("Nazwa użytkownika jest zajęta.")
    return error_messages


def validate_passwords(password: str, repeat_password: str) -> List[str]:
    error_messages: List[str] = []
    if len(password) < 8:
        error_messages.append(
            "Hasło musi mieć więcej niż 8 znaków.")
    if password != repeat_password:
        error_messages.append("Hasła się nie zgadzają.")
    if not re.search(r'\d', password):
        error_messages.append(
            "Hasło musi zawierać cyfrę.")
    if not re.search(r'[A-Z]', password):
        error_messages.append(
            "Hasło musi zawierać dużą literę.")
    if not re.search(r"[~`¿¡!#$%\^&*€£@+÷=\-\[\]\\';,/{}\(\)|\":<>\?\._]", password):
        error_messages.append(
            "Hasło musi zawierać znak specjalny.")
    return error_messages
