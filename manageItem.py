
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from store  import Store
from item import Item

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ManageItem(webapp2.RequestHandler):
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

            store = ndb.Key(urlsafe=id).get()
            items = Item.query(
                Item.store == store.key.id())
            access_link = users.create_logout_url("/")


            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "store": store,
                "items": items,
            }

            template = JINJA_ENVIRONMENT.get_template("items.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manageItem', ManageItem),
], debug=True)
