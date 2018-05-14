#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-06 10:57:04
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import time
from . import istpApi
from flask import g
from flask import jsonify
from flask import request
from flask_cors import cross_origin
from authentication import auth
from flask import Response
import simplejson
import time


@cross_origin()
@istpApi.route("/sources", methods=['GET'])
def get_sources():
    db = getattr(g, 'ISTP_DB')
    if db == None:
        return jsonify({"error": "can't connect to background database service."}), 503
    condition = {}
    instrument_type = request.args.get("instrument_type", None)
    if instrument_type != None:
        condition["Instrument_type"] = instrument_type
    sources = db.get_element_and_full_list("Source_name", condition)
    if sources == False:
        return jsonify({"error": "background database service error."}), 503
    return jsonify({"sources": sources})


@cross_origin()
@istpApi.route("/instrument_types", methods=['GET'])
def get_instrument_types():
    db = getattr(g, 'ISTP_DB', None)
    if db == None:
        return jsonify({"error": "can't connect to background database service."}), 503
    condition = {}
    source_name = request.args.get("source_name", None)
    if source_name != None:
        condition["Source_name"] = source_name
    instrument_types = db.get_element_list("Instrument_type", condition)
    if instrument_types == False:
        return jsonify({"error": "background database service error."}), 503
    return jsonify({"instrument_types": instrument_types})


@cross_origin()
@istpApi.route("/instruments", methods=['GET'])
def get_instruments():
    db = getattr(g, 'ISTP_DB', None)
    if db == None:
        return jsonify({"error": "can't connect to background database service."}), 503
    condition = {}
    source_name = request.args.get("source_name", None)
    if source_name != None:
        condition["Source_name"] = source_name
    instrument_type = request.args.get("instrument_type", None)
    if instrument_type != None:
        condition["Instrument_type"] = instrument_type
    instruments = db.get_element_and_full_list("Descriptor", condition)
    if instruments == False:
        return jsonify({"error": "background database service error."}), 503
    return jsonify({"instruments": instruments})


@cross_origin()
@istpApi.route("/data_sets", methods=['GET'])
def get_data_sets():
    db = getattr(g, 'ISTP_DB', None)
    if db == None:
        return jsonify({"error": "can't connect to background database service."}), 503
    condition = {}
    source_name = request.args.get("source_name", None)
    if source_name != None:
        condition["Source_name"] = source_name
    instrument_type = request.args.get("instrument_type", None)
    if instrument_type != None:
        condition["Instrument_type"] = instrument_type
    instrument = request.args.get("instrument")
    if instrument != None:
        condition["Descriptor"] = instrument
    data_sets = db.get_data_sets(condition)
    if data_sets == False:
        return jsonify({"error": "background database service error."}), 503
    return jsonify({"data_sets": data_sets})


@cross_origin()
@istpApi.route("/data_sets/<data_set>/variables", methods=['GET'])
def get_data_set_variables(data_set):
    db = getattr(g, 'ISTP_DB', None)
    if db == None:
        return jsonify({"error": "can't connect to background database service."}), 503
    var_list = db.get_variables(data_set, "data")
    if var_list == False:
        return jsonify({"error": "background database service error."}), 503
    return jsonify({"variables": var_list})


@cross_origin()
@istpApi.route("/data_sets/<data_set>/data", methods=['GET'])
# @auth.login_required
def get_data(data_set):
    db = getattr(g, 'ISTP_DB', None)
    if db == None:
        return jsonify({"error": "can't connect to background database service."}), 503

    if not (("start_time" in request.args) ^ ("end_time" in request.args)):
        start_time = request.args.get("start_time", None)
        end_time = request.args.get("end_time", None)
        if start_time != None and end_time != None:
            try:
                start_time = time.mktime(time.strptime(
                    start_time, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                return jsonify({"error": "start_time:" + start_time + " doesn't match '%Y-%m-%d %H:%M:%S'."}), 400
            try:
                end_time = time.mktime(time.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                return jsonify({"error": "end_time:" + end_time + " doesn't match '%Y-%m-%d %H:%M:%S'."}), 400
            if start_time > end_time:
                return jsonify({"error": "please check time range, start_time can't over end_time."}), 400
    else:
        return jsonify({"error": "start_time and end_time must appeared together."}), 400

    variables = request.args.get("variables", None)
    if variables == None:
        return jsonify({"error": "variables"}), 400
    variables = variables.split(",")

    attrs, data = db.get_data(data_set, variables, start_time, end_time)
    if attrs == False:
        return jsonify({"error": "background database service error."}), 503
    elif "error" in attrs:
        return jsonify(attrs)

    try:
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "can not convert offset:%s to int." % request.args.get("offset")}), 400
    if offset < 0:
        return jsonify({"error": "offset:%d isn't a nonnegative number." % offset}), 400

    try:
        number = int(request.args.get('number', 1000))
    except ValueError:
        return jsonify({"error": "can not convert number:%s to int." % request.args.get('number')}), 400
    if number <= 0:
        return jsonify({"error": "number:%d isn't a positive number." % number}), 400
    # elif number > 100000:
    #     return jsonify({"error": "the max number is 100000."}), 400

    try:
        data = list(data[offset:offset + number])
    except Exception as e:
        return jsonify({"error": "background database service error."}), 503

    response = Response(mimetype='application/json')
    count = len(data)
    result = simplejson.dumps(
        {"attrs": attrs, "data": data, "count": count}, ignore_nan=True)
    response.set_data(result)
    return response
