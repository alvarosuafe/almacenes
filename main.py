
from google.appengine.api import users
from mainMenu import MainMenuHandler
from storeAdd import AddStore
from storeModify import StoreModify
from storeDelete import StoreDelete
from manageItem import ManageItem
from itemsAdd import ItemsAdd
from itemModify import ItemModify
from itemDelete import ItemDelete

import os
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user_name = "Empezar"
        user = users.get_current_user()
        if user != None:
                self.redirect("/mainMenu")
		return
        else:
                access_link = users.create_login_url("/mainMenu")

        template_values = {
                "user_name": user_name,
                "access_link": access_link,
        }

        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render(template_values));

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/mainMenu", MainMenuHandler),
    ("/storeAdd", AddStore),
    ("/storeModify", StoreModify),
    ("/storeDelete", StoreDelete),
    ("/manageItem", ManageItem),
    ("/itemsAdd", ItemsAdd),
    ("/itemModify", ItemModify),
    ("/itemDelete", ItemDelete)
], debug=True)
