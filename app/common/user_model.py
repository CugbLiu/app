#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-09 17:36:16
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import time
import bcrypt
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from user_db import USER_DB


class AnonymousUser():
    @property
    def is_anonymous(self):
        return True

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class User(object):

    def __init__(self, username, email, password, confirmed=False):
        self.username = username
        self.email = email
        self.password_hash = str(password)
        self.confirmed = confirmed
        self.db = USER_DB()

    @property
    def password(self, password):
        raise AttributeError('password is not a readable attribute')

    def set_password(self, password):
        return bcrypt.hashpw(str(password), bcrypt.gensalt())

    def verify_password(self, password):
        if bcrypt.hashpw(str(password), self.password_hash) == self.password_hash:
            return True
        else:
            return False

    def generate_confirmation_token(self, expiration=43200):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.email})

    @staticmethod
    def confirm(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        email = data.get('confirm', None)
        return email

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        session_time = time.time()
        token = s.dumps(
            {'id': self.email, 'time_stamp': session_time}).decode('ascii')
        self.is_login = True
        return token

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = self.db.query_by_email(data['id'])
        if u is None or u == False:
            return u
        else:
            user = User(u['username'], u['email'], u['password'])
        return user

    def __str__(self):
        return self.username + ':' + self.email

    def __repr__(self):
        return self.username + ':' + self.email
