
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
from store import Store
from item import Item

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ItemDelete(webapp2.RequestHandler):

    def get(self):
        try:
            id = self.request.GET['item_id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=serie was not found")
            return

        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                item = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "item": item,
            }

            template = JINJA_ENVIRONMENT.get_template("itemDelete.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")


    def post(self):
            try:
                id = self.request.GET['item_id']
            except:
                self.redirect("/error?msg=Key missing for deletion.")
                return

            user = users.get_current_user()

            if user and id:
                try:
                    item = ndb.Key(urlsafe=id).get()
                except:
                    self.redirect("/error?msg=Key was not found.")
                    return

                item.key.delete();
                self.redirect("/mainMenu")
            else:
                self.redirect("/")

