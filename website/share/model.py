from django.core.urlresolvers import reverse

from modularodm import Q, fields
from modularodm.exceptions import NoResultsFound
from modularodm.query.query import RawQuery
from modularodm.storage.mongostorage import MongoQuerySet


class ShareFilesList(list):
    pass

class ShareQuerySet(MongoQuerySet):
    pass

class Share(object):

    attribue_map = {
        '_id': '_id',
        'title': 'Share Window',
    }

    def __init__(self,node=None):
        if node is None:
            return
        self.node = node
        setattr(self.node, 'category', 'share window')
        self.node.is_public = True

    def __getattr__(self, item):
        return getattr(self.node, item)

    def __eq__(self,other):
        if not isinstance(other,self.__class__):
            return False
        return self._id == other._id

    def save(self):
        # for key, value in self.attribue_map.iteritems():
        #     if getattr(self,key) != getattr(self.node,value):
        #         setattr(self.node,value, getattr(self,key))
        self.node.save()

    def __repr__(self):
        return '<User ({}) share files with id \'{}\'>'.format(self.name,self._id)

    @property
    def pk(self):
        return self._id

    @property
    def api_v2_url(self):
        return reverse('project:{}:share_window'.format(self._id), kwargs={'_id': self._id})

    @property
    def absolute_api_v2_url(self):
        from api.base.utils import absolute_reverse
        return absolute_reverse('project:{}:share_window'.format(self._id), kwargs={'_id': self._id})
