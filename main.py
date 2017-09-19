#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler): # glavni handler odpre datoteko "index.html"
    def get(self):
        return self.render_template("index.html")

class LotoHandler(BaseHandler):
    def get(self):
        numberOfNumbers=8
        listOfNumbers = []                               # seznam nakljucnih stevil, zaenkrat prazen
        while numberOfNumbers > len(listOfNumbers):      # dokler je seznam krajsi od vrednosti vnesenega stevila, ponavljaj ukaze v zanki
            found = False                                # s to spremenljivko bomo opazovali ali se neko stevilo ze nahaja v nasem seznamu
            someRandom = random.randint(1,39)            # v to spremenljivko shranimo nakljucno stevilo
            if len(listOfNumbers) == 0:                  # v kolikor je seznam prazen...
                listOfNumbers.append(someRandom)         # prvo nakljucno stevilo avtomatsko shranimo vanj
            else:                                        # v kolikor je v seznamu ze kaksno stevilo...
                for y in listOfNumbers:                  # pa se sprehodi skozi seznam...
                    if someRandom == y:                  # ter primerjaj vsako vrednost z vrednostjo nakljucnega stevila
                        found = True                     # ce se ujemata, spremeni to spremenljivko v true
                        break                            # ter prekini sprehod po seznamu
                if found == False:                       # ce stevila nismo nasli v seznamu...
                    listOfNumbers.append(someRandom)     # potem ga le temu dodamo

        params = {"list": listOfNumbers} # seznam shranimo v parametre...
        return self.render_template("loto.html",params) # in jih podamo skupaj s spletno stranjo, ki jo bo handler odprl

app = webapp2.WSGIApplication([  # poti
    webapp2.Route('/', MainHandler),
    webapp2.Route("/loto", LotoHandler),
], debug=True)
