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
        "tools.staticfile.root": path
    },
    "/bootstrap.min.css": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "css/bootstrap.min.css"
    },
    "/bootstrap-responsive.min.css": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "css/bootstrap-responsive.min.css"
    }
})
