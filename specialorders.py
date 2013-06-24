import cherrypy
import sqlite3 as lite
from mako.lookup import TemplateLookup
import os.path


path = os.path.abspath(os.path.dirname(__file__))
lookup = TemplateLookup(directories=[path + "/templates/"])


class SpecialOrders(object):
    @cherrypy.expose
    def index(self):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Orders WHERE Status=\"Pending\"")
            orders = cur.fetchall()

            cur.execute("SELECT * FROM Orders WHERE Status=\"Ordered\"")
            orders += cur.fetchall()

            cur.execute("SELECT * FROM Orders WHERE Status=\"Here\"")
            orders += cur.fetchall()

        template = lookup.get_template("orders.txt")
        return template.render(orders=orders, url="/")

    @cherrypy.expose
    def add_item(self, distributor="", part_number="", part_desc="", price="",
                 customer="", cust_phone="", status="Pending"):

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

            # Add the item to the database
            cur.execute("""INSERT INTO Orders VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", (id,
                        distributor, part_number, part_desc, price, customer, cust_phone,
                        status))

        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def delete_item(self, id=None, url="/"):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Orders WHERE Id=?", (id,))

        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def change_status(self, id=None, status="Pending", url="/"):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("UPDATE Orders SET Status=? WHERE Id=?", (status, id))

        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def search(self, query=""):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM Orders")

            orders = cur.fetchall()

        results = set()
        for o in orders:
            for i in range(1, len(o)):
                if query.lower() in str(o[i]).lower():
                    results.add(o)

        template = lookup.get_template("search.txt")
        return template.render(query=query, orders=results, url="/search?query=" + query)


# Initialize the database
con = lite.connect("orders.db")
with con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Orders(Id INT, Distributor TEXT,
                PartNumber TEXT, PartDesc TEXT, Price TEXT, Customer TEXT, CustPhone TEXT,
                Status TEXT)""")


# Start the cherrypy server
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
