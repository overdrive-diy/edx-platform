"""
Helper methods related to EdxNotes.
"""
import json
import requests
from uuid import uuid4
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# To start stub server on devstack:
# cd common/djangoapps/terrain
# python -m stubs.start edxnotes 8042
# Uncomment function `create_notes(20, username, unicode(course_id).encode('utf-8'))`
# to create 20 notes for the user in the course and refresh Notes page.
# !!! Do not forget comment it out again after that and restart the server.

# TODO: Remove this function before merge!!!
def _get_dummy_notes(count=1, user="dummy-user-id", course_id="dummy-course-id"):
    """
    Returns a list of dummy notes.
    """
    return [_get_dummy_note(user=user, course_id=course_id) for i in xrange(count)]  # pylint: disable=unused-variable


# TODO: Remove this function before merge!!!
def _get_dummy_note(user="dummy-user-id", course_id="dummy-course-id"):
    """
    Returns a single dummy note.
    """
    nid = uuid4().hex
    return {
        "id": nid,
        "created": "2014-10-31T10:05:00.000000",
        "updated": "2014-10-31T10:50:00.101010",
        "user": user,
        "usage_id": "dummy-usage-id",
        "course_id": course_id,
        "text": "dummy note text " + nid,
        "quote": "dummy note quote",
        "ranges": [
            {
                "start": "/p[1]",
                "end": "/p[1]",
                "startOffset": 0,
                "endOffset": 10,
            }
        ],
    }


# TODO: Remove this function before merge!!!
def create_notes(count, user, course_id):
    dummy_notes = _get_dummy_notes(count=count, user=user, course_id=course_id)
    requests.post(settings.EDXNOTES_INTERFACE["url"] + "create_notes", data=json.dumps(dummy_notes))


def get_token():
    return None


def get_notes(username, course_id):
    # TODO: Remove this line before merge!!!
    # create_notes(20, username, unicode(course_id).encode('utf-8'))
    url = get_storage_url() + "/search"
    response = requests.get(url, params={
        'user': username,
        'course_id': unicode(course_id).encode('utf-8'),
    })
    return response.content


def get_storage_url():
    """
    Returns endpoint.
    """
    interface = settings.EDXNOTES_INTERFACE if hasattr(settings, 'EDXNOTES_INTERFACE') else False
    if interface and interface.get("url", False):
        url = interface["url"]
        if not url.endswith("/"):
            url += "/"
        return url + "api/v1"
    else:
        raise ImproperlyConfigured("No endpoint was provided for EdxNotes.")


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
