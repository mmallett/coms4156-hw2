#!/usr/bin/env python2.7

import os
import sys

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

from models import messages_model

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgres://cwuepekp:SkVXF4KcwLJvTNKT41e7ruWQDcF3OSEU@jumbo.db.elephantsql.com:5432/cwuepekp"
engine = create_engine(DATABASEURI)
try:
    print 'creating tables'
    myconn = engine.connect()
    messages = messages_model.Messages(myconn)
    messages.init_messages()
    myconn.close()
except Exception as e:
    print e
    print 'WE CANT CREATE THE TABLE ABORt!!!! :('
    sys.exit()

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print "can't connect to db"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except:
    print 'failed to safely close db connection'


def _do_get():
    model = messages_model.Messages(g.conn)

    messages = model.get_messages()

    return render_template('messages.html', messages=messages)

def _do_post(request):
    model = messages_model.Messages(g.conn)

    message = request.form['message']

    model.create_message(message)

    # messages = model.get_messages()

    return render_template('message-created.html')

# GET /
#   read all the messages render the template
# POST /
#   create the new message re-render all messages template
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'GET':
            return _do_get()
        else:
            return _do_post(request)

    except:
        import traceback; traceback.print_exc()

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):

    HOST, PORT = host, port
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)


  run()
