from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings
from edxmako.shortcuts import render_to_response
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_with_access
from edxnotes.helpers import (
    get_storage_url,
    edxnotes_enabled_for_course
)


@login_required
def edxnotes(request, course_id):
    ''' Displays the edx notes. '''
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_with_access(request.user, 'load', course_key)

    if not edxnotes_enabled_for_course(course):
        raise Http404

    context = {
        # Use camelCase to name keys.
        'course': course,
        'storage': get_storage_url(),
        'token': '',
        'debug': settings.DEBUG,
    }

    return render_to_response('edxnotes.html', context)
