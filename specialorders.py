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
    def add_item(self, distributor="", part_number="", part_desc="", customer="",
                 cust_phone=""):

        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()

            # Find a unique ID
            id = 1
            while True:
                cur.execute("SELECT * FROM Orders WHERE Id=?", (id,))
                if len(cur.fetchall()) is 0:
                    break
                else:
                    id += 1

            cur.execute("""INSERT INTO Orders VALUES(?, ?, ?, ?, ?, ?)""", (id,
                        distributor, part_number, part_desc, customer, cust_phone))

        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def delete_item(self, id=None):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Orders WHERE Id=?", (id,))

        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def search(self, query=""):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM Orders")

            orders = cur.fetchall()

        results = set()
        for o in orders:
            for f in o:
                if str(f).lower() == query.lower():
                    results.add(o)

        template = Template(filename="templates/search.txt")
        return template.render(query=query, orders=results)


# Initialize the database
con = lite.connect("orders.db")
with con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Orders(Id INT, Distributor TEXT,
                PartNumber TEXT, PartDesc TEXT, Customer TEXT, CustPhone TEXT)""")


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
