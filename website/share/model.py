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

    attribute_map = {
        '_id': '_id',
        'title':'Share Window',
        'category':'share window'
    }

    def __init__(self,*args, **kwargs):
        from website.project.model import Node
        create_or = kwargs.pop('creator', [])
        if create_or:
            self.node = Node(creator=create_or)
        else:
            return
        # setattr(self.node, 'category', 'share window')
        self.node.is_public = True
        for key, value in self.attribute_map.iteritems():
            setattr(self.node, key, value)

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

    @classmethod
    def load(cls, key):
        from website.models import Node
        try:
            node = Node.find_one(Q('public_file', 'eq', key))
            return cls(node)
        except NoResultsFound:
            return None

    @classmethod
    def find(cls, query=None, deleted=False, **kwargs):
        pass
        # from website.models import Node  # done to prevent import error
        # if query and getattr(query, 'nodes', False):
        #     for node in query.nodes:
        #         replacement_attr = cls.attribute_map.get(node.attribute, False)
        #         node.attribute = replacement_attr or node.attribute
        # elif isinstance(query, RawQuery):
        #     replacement_attr = cls.attribute_map.get(query.attribute, False)
        #     query.attribute = replacement_attr or query.attribute
        # query = query & Q('institution_id', 'ne', None) if query else Q('institution_id', 'ne', None)
        # query = query & Q('is_deleted', 'ne', True) if not deleted else query
        # nodes = Node.find(query, allow_institution=True, **kwargs)
        # return InstitutionQuerySet(nodes)

    @classmethod
    def find_one(cls, query=None, deleted=False, **kwargs):
        pass
        # from website.models import Node
        # if query and getattr(query, 'nodes', False):
        #     for node in query.nodes:
        #         replacement_attr = cls.attribute_map.get(node.attribute, False)
        #         node.attribute = replacement_attr if replacement_attr else node.attribute
        # elif isinstance(query, RawQuery):
        #     replacement_attr = cls.attribute_map.get(query.attribute, False)
        #     query.attribute = replacement_attr if replacement_attr else query.attribute
        # query = query & Q('institution_id', 'ne', None) if query else Q('institution_id', 'ne', None)
        # query = query & Q('is_deleted', 'ne', True) if not deleted else query
        # node = Node.find_one(query, allow_institution=True, **kwargs)
        # return cls(node)

    @property
    def pk(self):
        return self._id

    @property
    def api_v2_url(self):
        return reverse('project:share_window', kwargs={'_id': self._id})

    @property
    def absolute_api_v2_url(self):
        from api.base.utils import absolute_reverse
        return absolute_reverse('project:share_window', kwargs={'_id': self._id})
