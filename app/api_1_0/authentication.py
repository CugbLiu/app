#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-14 22:52:35
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from flask import g
from flask_httpauth import HTTPBasicAuth

from errors import unauthorized
from app.common.user_model import User,AnonymousUser
from app.common.user_db import USER_DB



auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return False

    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        if g.current_user:
            return True
        else:
            return False

    db = USER_DB()
    u = db.query_by_email(email_or_token)

    if u == False:
        return False
    elif u == None:
        return False
    else:
        user = User(u['username'], u['email'], u['password'])

    g.current_user = user
    g.token_used = False
    return user.verify_password(str(password))


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')
