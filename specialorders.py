import cherrypy
import sqlite3 as lite
from mako.template import Template
import os.path


class SpecialOrders(object):
    @cherrypy.expose
    def index(self):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Orders")

            orders = cur.fetchall()

        template = Template(filename="templates/orders.txt")
        return template.render(orders=orders)

    @cherrypy.expose
    def add_item(self, id=1, description=""):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Orders VALUES(?, ?)", (id, description))

        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def delete_item(self, id=None):
        id = (id,)
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Orders WHERE Id=?", id)

        raise cherrypy.HTTPRedirect("/")


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
        "tools.staticdir.root": path,
        "tools.staticfile.root": path
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
    },
    "/favicon.png": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "favicon.png"
    }
})
