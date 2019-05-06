
from google.appengine.api import users
from google.appengine.ext import ndb

from store import Store

import time
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class StoreModify(webapp2.RequestHandler):
    def get(self):
        try:
    	    id = self.request.GET['store_id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=store was not found")
            return

        user = users.get_current_user()

    	if user != None:
    		user_name = user.nickname()
    		access_link = users.create_logout_url("/")

    		try:
    			store = ndb.Key(urlsafe = id).get()
    		except:
    			self.redirect("/error?msg=key does not exist")
    			return

    		template_values = {
    			"user_name": user_name,
    			"access_link": access_link,
    			"store": store,
    		}

    		template = JINJA_ENVIRONMENT.get_template( "modifyStore.html" )
    		self.response.write(template.render(template_values));
    	else:
    		self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['store_id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=missing id for modification")
            return

    	user = users.get_current_user()

    	if user != None:
            # Get serie by key
    		try:
    			store = ndb.Key(urlsafe = id).get()
    		except:
    			self.redirect("/error?msg=key does not exist")
    			return


    		store.name = self.request.get("stName").strip()
    		store.description = self.request.get("stDescription").strip()


    		# Chk
    		if len(store.name) < 1:
				self.redirect("/error?msg=" + "Modification aborted: serie's name is mandatory")
				return

            # Save
    		store.put()
    		time.sleep(1)
    		self.redirect("/mainMenu")
    	else:
    		self.redirect("/")
