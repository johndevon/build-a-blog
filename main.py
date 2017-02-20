import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class BlogHome(Handler):
    def get(self):
        self.render('home.html')

class NewPost(Handler):
    def render_front(self, title="", body="", pageerror=""):

        self.render("newpost.html", title1=title, body1=body, pageerror1=pageerror)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            p = Post(title=title, body=body)
            p.put()

            self.redirect("/")
        else:
            error = "We need a title and a body"
            self.render_front(title, body, error)


app = webapp2.WSGIApplication([
    ('/', BlogHome),
    ('/NewPost', NewPost)
], debug=True)
