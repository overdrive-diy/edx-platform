"""
Views related to EdxNotes.
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings
from edxmako.shortcuts import render_to_response
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_with_access
from edxnotes.helpers import (
    get_storage_url,
    get_token,
    get_notes,
    edxnotes_enabled_for_course
)


@login_required
def edxnotes(request, course_id):
    """ Displays the EdxNotes page. """
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_with_access(request.user, "load", course_key)

    if not edxnotes_enabled_for_course(course):
        raise Http404

    notes = get_notes(request.user.username, course)
    context = {
        # Use camelCase to name keys.
        "course": course,
        "storage": get_storage_url(),
        "notes": notes,
        "token": get_token(),
        "debug": settings.DEBUG,
    }

    return render_to_response("edxnotes.html", context)
