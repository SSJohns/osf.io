
from rest_framework.renderers import JSONRenderer

class JSONAPIRenderer(JSONRenderer):
    format = "jsonapi"
    media_type = 'application/vnd.api+json; ext="bulk"'
