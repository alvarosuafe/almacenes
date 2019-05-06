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

class MainMenuHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

	if user != None:
		user_name = user.nickname()
		stores = Store.query(Store.user == user.user_id()).order(-Store.added)
		access_link = users.create_logout_url("/")

		template_values = {
			"user_name": user_name,
			"access_link": access_link,
			"stores": stores
		}

		template = JINJA_ENVIRONMENT.get_template("mainMenu.html" )
		self.response.write(template.render(template_values));
	else:
		self.redirect("/")

app = webapp2.WSGIApplication([
    ('/mainMenu', MainMenuHandler),
], debug=True)