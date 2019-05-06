

from google.appengine.api import users
from google.appengine.ext import ndb


from store import Store
from item import Item
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ItemsAdd(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            try:
                id = self.request.GET['store_id']
            except:
                id = None

            if not id:
                self.redirect("/error?msg=Key missing for management.")
                return
            access_link = users.create_logout_url("/")
            store = ndb.Key(urlsafe=id).get()
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "store": store
            }
            template = JINJA_ENVIRONMENT.get_template("itemsAdd.html")
            self.response.write(template.render(template_values));

        else:
             self.redirect("/")

    def post(self):
        user = users.get_current_user()

        id = self.request.get("id_store").strip()
        store = ndb.Key(urlsafe=id).get()
        if user != None:
            item = Item()
            item.store = store.key.id()
            item.user = user.user_id()
            item.name = self.request.get("stName").strip()
            item.amount = int(self.request.get("stAmount"))

            # Save
            item.put()

            self.redirect("/mainMenu")
        else:
            self.redirect("/")




