from panel.models import Semester


def get_initial_semester_id() -> int:
    try:
        s = Semester.objects.get(pk=15)
        return s.pk
    except Semester.DoesNotExist:
        s = Semester.objects.all().first()
        if s:
            return s.pk
        return -1
