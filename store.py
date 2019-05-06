
from google.appengine.ext import ndb


class Store(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True)
    user = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.StringProperty(required=True, indexed=True)
