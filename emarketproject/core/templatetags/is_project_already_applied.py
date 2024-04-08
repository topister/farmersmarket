from django import template

from core.models import Applicant

register = template.Library()


@register.simple_tag(name='is_project_already_applied')
def is_project_already_applied(project, user):
    applied = Applicant.objects.filter(project=project, user=user)
    if applied:
        return True
    else:
        return False
