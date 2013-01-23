from google.appengine.ext import db

class FSUser(db.Model):
    login = db.StringProperty()
    data = db.TextProperty()