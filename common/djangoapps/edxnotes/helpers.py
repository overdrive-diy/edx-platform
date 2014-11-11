"""
Helper methods related to EdxNotes.
"""
import json
import requests
import logging
from uuid import uuid4
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from xmodule.modulestore.django import modulestore
from lms.lib.xblock.runtime import unquote_slashes
from xmodule.modulestore.exceptions import ItemNotFoundError
# TODO: Remove these imports before merge!!!
from lms.lib.xblock.runtime import quote_slashes
import random
# end TODO

log = logging.getLogger(__name__)


# To start stub server on devstack:
# cd common/djangoapps/terrain
# python -m stubs.start edxnotes 8042
# Uncomment function `create_notes(20, username, unicode(course_id).encode('utf-8'))`
# to create 20 notes for the user in the course and refresh Notes page.
# !!! Do not forget comment it out again after that and restart the server.

# TODO: Remove this function before merge!!!
def _get_dummy_notes(count, user, course):
    """
    Returns a list of dummy notes.
    """
    html_modules = modulestore().get_items(
        course.id, qualifiers={
            'category': 'html',
        },
    )
    usage_keys = [quote_slashes(unicode(module.scope_ids.usage_id)) for module in html_modules]
    return [_get_dummy_note(user=user, course_id=unicode(course.id), usage_keys=usage_keys) for i in xrange(count)]  # pylint: disable=unused-variable
# end TODO


# TODO: Remove this function before merge!!!
def _get_dummy_note(user="dummy-user-id", course_id="dummy-course-id", usage_keys=[]):
    """
    Returns a single dummy note.
    """
    nid = uuid4().hex
    text = (
        "Lorem Ipsum is simply dummy text of the printing and typesetting"
        "industry. Lorem Ipsum has been the industry's standard dummy text ever"
        "since the 1500s, when an unknown printer took a galley of type and"
        "scrambled it to make a type specimen book. It has survived not only"
        "five centuries, but also the leap into electronic typesetting, remaining"
        "essentially unchanged. It was popularised in the 1960s with the release"
        "of Letraset sheets containing Lorem Ipsum passages, and more recently"
        "with desktop publishing software like Aldus PageMaker including"
        "versions of Lorem Ipsum."
    )
    quote = (
        "Lorem Ipsum is simply dummy text of the printing and typesetting"
        "industry. Lorem Ipsum has been the industry's standard dummy text ever"
        "since the 1500s, when an unknown printer took a galley of type and"
        "scrambled it to make a type specimen book."
    )

    return {
        "id": nid,
        "user": user,
        "usage_id": random.choice(usage_keys),
        "course_id": course_id,
        "text": text,
        "quote": quote,
        "ranges": [
            {
                "start": "/p[1]",
                "end": "/p[1]",
                "startOffset": 0,
                "endOffset": 10,
            }
        ],
    }
# end TODO


# TODO: Remove this function before merge!!!
def create_notes(count, user, course):
    dummy_notes = _get_dummy_notes(count, user, course)
    requests.post(settings.EDXNOTES_INTERFACE["url"] + "create_notes", data=json.dumps(dummy_notes))
# end TODO


def get_token():
    """
    Returns authentication token.
    """
    return None


def get_notes(username, course):
    """
    Returns all notes for the user.
    """
    # TODO: Remove this line before merge!!!
    # create_notes(20, username, course)
    # end TODO
    url = get_storage_url("/annotations")
    response = requests.get(url, params={
        'user': username,
        'course_id': unicode(course.id).encode('utf-8'),
    })

    try:
        collection = json.loads(response.content)
    except ValueError:
        return json.dumps([])

    # if collection is empty, just return it.
    if not collection:
        return response.content

    store = modulestore()
    with store.bulk_operations(course.id):
        for model in collection:
            unquoted_usage_key_string = unquote_slashes(model['usage_id'])
            usage_key = course.id.make_usage_key_from_deprecated_string(unquoted_usage_key_string)
            display_name, url = get_parent_info(course, store, usage_key)
            model.update({
                'unit': {
                    'display_name': display_name,
                    'url': url,
                }
            })

    return json.dumps(collection)


def get_parent(store, child_location):
    """
    Returns parent module for the passed `child_location`.
    """
    location = store.get_parent_location(child_location)
    if not location:
        log.warning("Parent location for the module not found: %s", child_location)
        return
    try:
        return store.get_item(location)
    except ItemNotFoundError:
        log.warning("Parent module not found: %s", location)
        return


def get_parent_info(course, store, child_location):
    """
    Returns dispay_name and url for the parent module.
    """
    parent = get_parent(store, child_location)

    if not parent:
        return (None, None)

    display_name = parent.display_name_with_default
    url = reverse('jump_to', kwargs={
        'course_id': course.id.to_deprecated_string(),
        'location': parent.location.to_deprecated_string(),
    })

    return (display_name, url)


def get_storage_url(path=""):
    """
    Returns endpoint.
    """
    interface = settings.EDXNOTES_INTERFACE if hasattr(settings, 'EDXNOTES_INTERFACE') else False
    if interface and interface.get("url", False):
        url = interface["url"]
        if not url.endswith("/"):
            url += "/"
        if not path.startswith("/"):
            path = "/" + path

        return url + "api/v1" + path
    else:
        raise ImproperlyConfigured(_("No endpoint was provided for EdxNotes."))


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
