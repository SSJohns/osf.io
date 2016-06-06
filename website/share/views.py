import httplib as http

from .model import Share
from framework.exceptions import HTTPError

def view_share_window(user_id, **kwargs):
    share = Share.load(user_id)
    if not share:
        raise HTTPError(http.NOT_FOUND)
    return {
        'id': share._id,
        'name': share.title
    }
