import sys
from rest_framework import serializers as ser

from api.base.serializers import JSONAPISerializer, IDField, TypeField, Link, LinksField, RelationshipField
from api.base.utils import absolute_reverse


class PublicFileSerializer(JSONAPISerializer):

    filterable_fields = frozenset([
        'name',
        'date_modified'
    ])

    id = IDField(source='_id', read_only=True)
    type = TypeField()
    name = ser.CharField(source='page_name')
    kind = ser.SerializerMethodField()
    size = ser.SerializerMethodField()
    path = ser.SerializerMethodField()
    materialized_path = ser.SerializerMethodField(method_name='get_path')
    date_modified = ser.DateTimeField(source='date')
    content_type = ser.SerializerMethodField()
    extra = ser.SerializerMethodField(help_text='Additional metadata about this wiki')

    user = RelationshipField(
        related_view='users:user-detail',
        related_view_kwargs={'user_id': '<user._id>'}
    )

    # LinksField.to_representation adds link to "self"
    links = LinksField({
        'info': Link('public_file:public_file-detail', kwargs={'user_id': '<_id>'}),
        'download': 'get_public_file_content'
    })

    class Meta:
        type_ = 'public_file'

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_path(self, obj):
        return '/{}'.format(obj)

    def get_kind(self, obj):
        return 'file'

    def get_size(self, obj):
        return sys.getsizeof(obj.content)

    def get_content_type(self, obj):
        return 'text/markdown'

    def get_public_file_content(self, obj):
        return absolute_reverse('public_file:public_file-content', kwargs={
            'user_id': obj._id,
        })


class PublicFileDetailSerializer(WikiSerializer):
    """
    Overrides Wiki Serializer to make id required.
    """
    id = IDField(source='_id', required=True)
