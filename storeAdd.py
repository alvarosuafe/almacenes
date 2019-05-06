

from google.appengine.api import users
from google.appengine.ext import ndb


from store import Store
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class AddStore(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
            }
            template = JINJA_ENVIRONMENT.get_template("storeAdd.html")
            self.response.write(template.render(template_values));

        else:
             self.redirect("/")

    def post(self):
        user = users.get_current_user()

        if user != None:
            store = Store()
            store.user = user.user_id()
            store.name = self.request.get("stName").strip()
            store.description = self.request.get("stDescription").strip()

            # Save
            store.put()

            self.redirect("/mainMenu")
        else:
            self.redirect("/")




