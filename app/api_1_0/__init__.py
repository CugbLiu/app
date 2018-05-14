#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-03 15:00:25
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import time
from flask import g
from flask_cors import cross_origin
from flask import Blueprint


iagaApi = Blueprint('iaga', __name__)
istpApi = Blueprint('istp', __name__)
userApi = Blueprint('main', __name__)
from . import iaga, istp, authentication, user, errors
from authentication import auth

@cross_origin()
@istpApi.before_request
def istp_before_request():
    pass
    # from app.common.istp_db import ISTP_DB
    # g.ISTP_DB = ISTP_DB()


@cross_origin()
@iagaApi.before_request
# @auth.login_required
def iaga_before_request():
    pass
    # from app.common.iaga_db import IAGA_DB
    # g.IAGA_DB = IAGA_DB()


@cross_origin()
@userApi.before_request
# @auth.login_required
def main_before_request():
    from app.common.user_db import USER_DB
    g.USER_DB = USER_DB()
