"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times
from loadrules import Rules

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

RULES=Rules(CONFIG.rules)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  flask.g.rules = RULES
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
def check(date):
  if(len(date) == 3):
    y = int(dt[0])
    m = int(dt[1])
    d = int(dt[2])
    try:
       datetime.date(y, m, d)
       return true
    except:
        return false
  elif (len(date) == 2):
    h = int(dt[0])
    m = int(dt[1])
    try:
       datetime.date(H, M)
       return true
    except:
        return false
    else:
        return false


@app.route("/_set_startdate")
def set_startdate():
  app.logger.debug("Got a JSON request");
  date = request.args.get('time', 0, type=str)
  dt = date.split('-')
  print("time:", date)
  res = {}
  if (check(dt)):
    flask.session["date"] = dt
    res["result"] = True
  else:
    res["result"] = False

  return jsonify(result=res)

@app.route("/_set_starttime")
def set_starttime():
  app.logger.debug("Got a JSON request");
  date = request.args.get('time', 0, type=str)
  print("time:", date)
  dt = date.split(':')
  print("time:", date)
  res = {}
  if (check(dt)):
    flask.session["time"] = dt
    res["result"] = True
  else:
    res["result"] = False

  return jsonify(result=res)

@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles.
  """
  app.logger.debug("Got a JSON request");
  miles = request.args.get('miles', 0, type=int)
  index = request.args.get('index', 0, type=int)
  speed_min = 0
  speed_max = 0
  for r in RULES:
    if miles < r[0]:
        speed_min = r[1]
        speed_max = r[2]
        break
  max_minute = miles*60*60 // speed_max
  min_minute = miles*60*60 // speed_min


  print("miles:", miles)
  print("index:", index)

  return jsonify(result=miles * 2)

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try:
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try:
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")


