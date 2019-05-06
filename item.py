
from google.appengine.ext import ndb


class Item(ndb.Model):
    store = ndb.IntegerProperty(required=True, indexed=True)
    added = ndb.DateProperty(auto_now_add=True)
    user = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    amount = ndb.IntegerProperty(required=True, indexed=True)

