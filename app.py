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
from rules import Rules

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
DATE=1
TIME=2

###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  flask.session.clear()
  flask.session['index'] = {}
  flask.session['control_point'] = 200
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
def checkinput(index, kilometers, res):
  if kilometers < 0 or kilometers > 1100:
    res['msg'] = """input %d invalid, should
                    between 200 and 1000
                 """ %(kilometers,)
    return False

  if kilometers > flask.session['control_point'] * 1.1:
    res['msg'] = """the control_point %d is over 1.1 longer
                    than the theoretical distance %d
                 """ % ( kilometers,
                         flask.session['control_point'])

    return False


  index_array = flask.session['index']

  next_item = str(index + 1)
  for i in range(0, index):
    item = str(i)

    if item not in index_array:
      res['msg'] = "Please input all below blank box!"
      return False

    if index_array[item]['distance'] >= kilometers:
      res['msg'] = "Please input in ascending order!"
      return False

    if next_item in index_array and \
        index_array[next_item]['distance'] <= kilometers:
      res['msg'] = "Please input in ascending order!"
      return False

  return True

def checktime(type, data):
  res = False
  if type == DATE:
    if len(data) == len("YYYY-MM-DD"):
      try:
        arrow.get(data, "YYYY-MM-DD")
        flask.session["date"] = data
        res = True
      except Exception as e:
        app.logger.error(str(e));
  elif type == TIME:
    if len(data) == len("HH-mm"):
      try:
        date = flask.session["date"]
        arrow.get(data, "HH:mm")
        flask.session["time"] = data
        res = True
      except Exception as e:
        app.logger.error(str(e));
  return res

def get_targettime(distance):
  min_minutes = 0
  max_minutes = 0
  min_minutes, max_minutes = RULES.calc_time(
          distance,
          flask.session['control_point'])
  open_time = ""
  close_time = ""
  if 'date' in flask.session and 'time' in flask.session:
    base = arrow.get(flask.session["date"] +
          " " + flask.session["time"],
          "YYYY-MM-DD HH:mm")
    open_time = base.replace(minutes = min_minutes).format(
           "MM/DD HH:mm")

    close_time = base.replace(minutes = max_minutes).format(
           "MM/DD HH:mm")

  return (open_time, close_time)


@app.route("/showlist")
def showlist():
    return flask.render_template('result.html')

@app.route("/_checkcontrol")
def checkcontrol():
  res = {}
  res["is_valid"] = False
  index = flask.session['index']
  if len(index) == 0:
    res['msg'] = "Please input distance in kilometers"
  else:
    list = [(k,index[k]) for k in sorted(index.keys())]
    if list[-1][1]['distance'] >= flask.session['control_point']:
      res['is_valid'] = True
    else:
      res['msg'] = "last distance %d should longer than control point %d"\
                    % (list[-1][1]['distance'],
                    flask.session['control_point'])

  return jsonify(result=res)

@app.route("/_startdate")
def set_startdate():
  res = {}
  res["is_valid"] = False
  data = request.args.get('time', 0, type=str).strip()
  if checktime(DATE, data):
    res["is_valid"] = True
  elif "date" in flask.session:
    del flask.session["date"]

  return jsonify(result=res)


@app.route("/_starttime")
def set_starttime():
  res = {}
  res["is_valid"] = False

  if "date" not in flask.session:
    res["msg"] = "Please input the date on left box first!"

  else:
    data = request.args.get('time', 0, type=str).strip()
    if checktime(TIME, data):
      res["is_valid"] = True
      open_time, close_time = get_targettime(0)
      res['open_time'] = open_time
      res['close_time'] = close_time
      flask.session['index']['0'] = {"opentime":open_time,
              "closetime":close_time,"distance":0}
    elif "time" in flask.session:
      del flask.session["time"]

  return jsonify(result=res)

@app.route("/_controlpoint")
def set_controlpoint():
  val = request.args.get('val', 0, type=int)
  res = {}
  res['is_valid'] = False
  if val in RULES.index:
    flask.session['control_point'] = val
    res['is_valid'] = True
  return jsonify(result=res)

@app.route("/_location")
def set_location():
  val = request.args.get('val', "", type=str)
  index = request.args.get('index', 0, type=int)
  res = {}
  res['is_valid'] = False
  if 'date' not in flask.session or 'time' not in flask.session:
    res['msg'] = "Please input date and time first!"

  elif str(index) not in flask.session['index'] or 'distance' not in flask.session['index'][str(index)]:
    res['msg'] = "Please input distance to left box first!"

  elif val == "":
    if 'location' in flask.session['index'][str(index)]:
      del flask.session['index'][str(index)]['location']

  else:
    flask.session['index'][str(index)]['location'] = val
    res['is_valid'] = True

  return jsonify(result=res)

@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from kilometers, using rules
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of kilometers, index.
  """
  res = {}
  res['is_valid'] = False
  app.logger.debug("Got a JSON request");
  kilometers = request.args.get('kilometers', 0, type=int)
  index = request.args.get('index', 0, type=int)

  if 'date' not in flask.session:
    res['msg'] = "date not set, should set first!"

  elif 'time' not in flask.session:
    res['msg'] = "time not set, should set first!"

  elif checkinput(index, kilometers, res):
    res['is_valid'] = True
    open_time, close_time = get_targettime(kilometers)
    flask.session['index'][str(index)] = {'distance':kilometers, 'opentime':open_time, 'closetime': close_time}

    res['open_time'] = open_time
    res['close_time'] = close_time

  elif str(index) in flask.session['index']:
    del flask.session['index'][str(index)]['distance']

  return jsonify(result=res)

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


