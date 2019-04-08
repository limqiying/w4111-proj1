import copy
#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://ss5645:password1234@34.73.21.127/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  # inventory_list_sql = "SELECT I.sku, I.name, I.description, I.quantity, I.price, AVG(R.rating) as average_rating," + \
  #   " COUNT(R.rating) as num_ratings" + \
  #   " FROM inventory I, review R" + \
  #   " WHERE I.sku = R.sku and CAST(I.quantity AS DEC)> 0" + \
  #   " GROUP BY I.sku, I.name, I.description, I.quantity, I.price"


  inventory_list_sql = """
    SELECT I.sku, I.name, I.description, I.quantity, I.price, AVG(R.rating) as average_rating,
    COUNT(R.rating) as num_ratings
    FROM inventory I LEFT JOIN review R on I.sku = R.sku
    WHERE CAST(I.quantity AS DEC)> 0
    GROUP BY I.sku, I.name, I.description, I.quantity, I.price
    """

  # print inventory_list_sql

  # get the inventory data
  cursor = g.conn.execute(inventory_list_sql)
  inventory_cols = cursor.keys()
  inventory_data = list(cursor)
  cursor.close()


  # money_spent_sql = "select * from (" + \
  #   "select x.name, sum(cast(x.price as integer)) as total_spending from (" + \
  #   "select c.name,cs.price from customer as c, buys as b, \"order\" as o, consists_of as cs where cast(c.cid as text) = b.cid " + \
  #   "and b.oid = o.oid and o.oid = cs.oid" + \
  #   ") as x group by name" + \
  #   ") as z order by z.total_spending desc"

  # cursor = g.conn.execute(money_spent_sql)
  # money_spent_cols = cursor.keys()
  # money_spent_data = list(cursor)
  # cursor.close()


  # sku_detail_sql = "select w.sku ,w.name, w.description, x.total_sale, y.average_rating from inventory as w LEFT JOIN (" + \
  #   "select a.sku, sum(cast(a.price as integer)) as total_sale from (" + \
  #   "select i.sku, cs.price from inventory as i, consists_of as cs where i.sku = cs.sku" + \
  #   ") as a group by sku" + \
  #   ") x ON w.sku = x.sku " + \
  #   "LEFT JOIN (" + \
  #   "select z.sku, avg(z.rating) as average_rating from (" + \
  #   "select i.sku, cast(r.rating as integer) as rating from inventory as i, review as r where i.sku = r.sku" + \
  #   ") as z group by sku" + \
  #   ") as y ON w.sku = y.sku order by w.sku asc"

  # cursor = g.conn.execute(sku_detail_sql)
  # sku_detail_cols = cursor.keys()
  # sku_detail_data = list(cursor)
  # cursor.close()


  # shipping_cost_sql = "select * from (" + \
  #   "select d.zip_code, avg(d.shipping_cost) as average_cost from (" + \
  #   "select ra.zip_code, cast(sd.shipping_cost as integer) from residential_address as ra, ships_to as st, \"order\" as o, ships_via as sv, shipping_detail as sd " + \
  #   "where cast(ra.aid as text) = cast(st.aid as text) and st.oid = o.oid and o.oid = sv.oid and cast(sv.shipid as text) = cast(sd.shipid as text)" + \
  #   ") as d group by zip_code" + \
  #   ") as c order by average_cost desc"

  # cursor = g.conn.execute(shipping_cost_sql)
  # shipping_cost_cols = cursor.keys()
  # shipping_cost_data = list(cursor)
  # cursor.close()

  # context = dict(
  #   inventory_cols = inventory_cols,
  #   inventory_data = inventory_data,
  #   money_spent_cols = money_spent_cols,
  #   money_spent_data = money_spent_data,
  #   sku_detail_cols = sku_detail_cols,
  #   sku_detail_data = sku_detail_data,
  #   shipping_cost_cols = shipping_cost_cols,
  #   shipping_cost_data = shipping_cost_data
  # )
  context = dict(
    inventory_cols = inventory_cols,
    inventory_data = inventory_data,
  )


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")



# Example of adding new data to the database
@app.route('/view_item_detail', methods=['POST'])
def view_item_detail():
  print request.form

  sku = request.form['sku']

  cursor = g.conn.execute("SELECT email FROM customer where name = '%s'" % (name))

  # g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)

  # cursor = g.conn.execute("SELECT name FROM customer")
  names = []
  for result in cursor:
    names.append(result['email'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("index.html", **context)
  # return redirect('/')

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  print request.form

  name = request.form['name']

  cursor = g.conn.execute("SELECT email FROM customer where name = '%s'" % (name))

  # g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)

  # cursor = g.conn.execute("SELECT name FROM customer")
  names = []
  for result in cursor:
    names.append(result['email'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("index.html", **context)
  # return redirect('/')


@app.route('/statistics', methods=['POST', 'GET'])
def statistics():

  min_cust_sale = 0
  if 'min_cust_sale' in request.form:
    min_cust_sale = request.form["min_cust_sale"]

  print "min_cust_sale = ", min_cust_sale

  money_spent_sql = """
    select * from (
    select x.name, sum(cast(x.price as integer)) as total_spending from (
    select c.name,cs.price from customer as c, buys as b, "order" as o, consists_of as cs where cast(c.cid as text) = b.cid 
    and b.oid = o.oid and o.oid = cs.oid
    ) as x group by name
    ) as z order by z.total_spending desc
    """

  cursor = g.conn.execute(money_spent_sql)
  money_spent_cols = cursor.keys()
  money_spent_data = list(cursor)
  cursor.close()


  sku_detail_sql = "select w.sku ,w.name, w.description, x.total_sale, y.average_rating from inventory as w LEFT JOIN (" + \
    "select a.sku, sum(cast(a.price as integer)) as total_sale from (" + \
    "select i.sku, cs.price from inventory as i, consists_of as cs where i.sku = cs.sku" + \
    ") as a group by sku" + \
    ") x ON w.sku = x.sku " + \
    "LEFT JOIN (" + \
    "select z.sku, avg(z.rating) as average_rating from (" + \
    "select i.sku, cast(r.rating as integer) as rating from inventory as i, review as r where i.sku = r.sku" + \
    ") as z group by sku" + \
    ") as y ON w.sku = y.sku order by w.sku asc"

  cursor = g.conn.execute(sku_detail_sql)
  sku_detail_cols = cursor.keys()
  sku_detail_data = list(cursor)
  cursor.close()


  shipping_cost_sql = "select * from (" + \
    "select d.zip_code, avg(d.shipping_cost) as average_cost from (" + \
    "select ra.zip_code, cast(sd.shipping_cost as integer) from residential_address as ra, ships_to as st, \"order\" as o, ships_via as sv, shipping_detail as sd " + \
    "where cast(ra.aid as text) = cast(st.aid as text) and st.oid = o.oid and o.oid = sv.oid and cast(sv.shipid as text) = cast(sd.shipid as text)" + \
    ") as d group by zip_code" + \
    ") as c order by average_cost desc"

  cursor = g.conn.execute(shipping_cost_sql)
  shipping_cost_cols = cursor.keys()
  shipping_cost_data = list(cursor)
  cursor.close()

  context = dict(
    money_spent_cols = money_spent_cols,
    money_spent_data = money_spent_data,
    sku_detail_cols = sku_detail_cols,
    sku_detail_data = sku_detail_data,
    shipping_cost_cols = shipping_cost_cols,
    shipping_cost_data = shipping_cost_data
  )


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("statistics.html", **context)

@app.route('/item', methods=['POST'])
def item():
  # print request.form
  
  sku = request.form['sku']
  query1 = "SELECT I.name, I.description, I.quantity, I.price FROM inventory I WHERE I.sku = '%s'" % (sku)
  query2 = "SELECT R.title, R.r_text, R.rating, R.date_posted, C.name FROM inventory I, review R, reviews RS, customer C WHERE I.sku = R.sku and RS.rid = R.rid and RS.cid = C.cid and I.sku = '%s'" % (sku)
  cursor = g.conn.execute(query1)

  result = cursor.fetchone()
  data = {key: result[key] for key in result.keys()}
  context = dict(data = data)

  cursor = g.conn.execute(query2)
  reviews = []
  for result in cursor:
    row = {key: result[key] for key in result.keys()}
    reviews.append(row)  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = data, reviews=reviews)
  return render_template("another.html", **context)
  # return redirect('/')

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
