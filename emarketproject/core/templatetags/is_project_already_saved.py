from django import template

from core.models import BookmarkProject

register = template.Library()


@register.simple_tag(name='is_project_already_saved')
def is_project_already_saved(project, user):
    applied = BookmarkProject.objects.filter(project=project, user=user)
    if applied:
        return True
    else:
        return False
