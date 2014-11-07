"""
Helper methods related to EdxNotes.
"""
import datetime
from uuid import uuid4
from django.conf import settings


def _now():
    """
    Returns current time in URC format.
    """
    return datetime.datetime.utcnow().replace(microsecond=0)


def get_storage_url():
    """
    Returns endpoint.
    """
    url = settings.EDXNOTES_INTERFACE["url"] or "/"
    if not url.endswith("/"):
        url += "/"
    return url + "api/v1"


def generate_uid():
    """
    Generates unique id.
    """
    return uuid4().int  # pylint: disable=no-member


def edxnotes_enabled_for_course(course):
    """
    Returns True if the edxnotes app is enabled for the course, False otherwise.

    In order for the app to be enabled it must be:
        1) enabled globally via FEATURES.
        2) present in the course tab configuration.
    """
    tab_found = next((True for t in course.tabs if t['type'] == 'edxnotes'), False)
    feature_enabled = settings.FEATURES.get('ENABLE_EDXNOTES')

    return feature_enabled and tab_found
