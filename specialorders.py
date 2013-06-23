import cherrypy
import sqlite3 as lite
from mako.template import Template
import os.path


class SpecialOrders(object):
    def index(self):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Orders")

            orders = cur.fetchall()

        template = Template(filename="templates/orders.txt")
        return template.render(orders=orders)

    index.exposed = True

    def add_item(self, number=1, description=""):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Orders VALUES(?, ?)", (number, description))

        raise cherrypy.HTTPRedirect("/")

    add_item.exposed = True


# Initialize the database
con = lite.connect("orders.db")
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Orders(Id INT, Item TEXT)")


# Start the cherrypy server
path = os.path.abspath(os.path.dirname(__file__))
cherrypy.quickstart(SpecialOrders(), "/", config={
    "global": {
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 9000,
        "tools.staticdir.root": path
    },
    "/css": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "css/"
    },
    "/img": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "img/"
    },
    "/js": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "js/"
    }
})
