import cherrypy
import sqlite3 as lite


class SpecialOrders(object):
    def index(self):
        con = lite.connect("orders.db")

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Orders")

            orders = cur.fetchall()

            return str(orders)

    index.exposed = True


# Initialize the database
con = lite.connect("orders.db")
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Orders(Id INT, Item TEXT)")


# Start the cherrypy server
cherrypy.config.update("cherrypy.conf")
cherrypy.quickstart(SpecialOrders())
