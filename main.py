#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, jinja2, os
import simple
from model.MyListener import *
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/main.html')
        self.response.write(template.render())

    def post(self):
        login = self.request.get('login')
        users = MyListener.all().fetch(200)

        my_user = None
        for user in users:
            if user.login == login:
                my_user = user
                break

        if not my_user:
            my_user = MyListener()
            my_user.login = login
            my_user.data = simple.getLove(login)
            my_user.put()
        self.redirect('/user/' + my_user.login)

class ListenerHandler(webapp2.RequestHandler):
    def get(self, login):
        users = MyListener.all().fetch(200)

        my_user = None
        for user in users:
            if user.login == login:
                my_user = user
                break
        template_values = {'info' : my_user.data}
        template = jinja_environment.get_template('templates/info.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('r*/user/(.*)', ListenerHandler)
                              ], debug=True)
