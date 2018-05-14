#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-08 20:03:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
from flask import request, jsonify
from . import userApi, istpApi, iagaApi


@userApi.app_errorhandler(404)
@istpApi.app_errorhandler(404)
@iagaApi.app_errorhandler(404)
def not_found(error=None):
    message = {
        'result': "error",
        'message': 'Not Found ' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@userApi.app_errorhandler(500)
@istpApi.app_errorhandler(500)
@iagaApi.app_errorhandler(500)
def internal_server_error():
    message = {
        'result': 'error',
        'message': 'internal server error'
    }
    response = jsonify(message)
    response.status_code = 500
    return response


def bad_request(message):
    response = jsonify({'result': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'result': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'result': 'forbidden', 'message': message})
    response.status_code = 403
    return response
