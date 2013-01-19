from google.appengine.ext import db

class MyListener(db.Model):
    login = db.StringProperty()
    data = db.TextProperty()