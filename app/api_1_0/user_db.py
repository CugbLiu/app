#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-09 18:13:37
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import time
from app import user_db
from settings import my_params

# user_db = 'USER'
# user_coll = 'user'
user_db_1 = my_params.user_db
user_coll = my_params.user_coll

class USER_DB:
    def __init__(self):
        self.conn = user_db[user_db_1]

    def query_by_email(self, email):
        try:
            return self.conn.get_collection(user_coll).find_one({'email': email})
        except Exception as e:
            return False

    def insert_user(self, user):
        u = {
            'username': user.username,
            'email': user.email,
            'password': user.password_hash,
            'confirmed': user.confirmed
        }
        try:
            self.conn.get_collection(user_coll).insert(u)
        except Exception as e:
            return False
        return True

    def reset_user_password(self, email, new_passwod):
        try:
            user = self.conn.get_collection(
                user_coll).find_one({'email': email})
        except Exception as e:
            return False
        if user is None:
            return user
        try:
            self.conn.get_collection(user_coll).update(
                {'email': email}, {"$set": {"password": new_passwod}})
        except Exception as e:
            return False
        return True

    def update_user_confirmed(self, email, confirmed):
        try:
            user = self.conn.get_collection(
                user_coll).find_one({'email': email})
        except Exception as e:
            return False
        if user is None:
            return user
        try:
            self.conn.get_collection(user_coll).update(
                {'email': email}, {"$set": {"confirmed": confirmed}})
        except Exception as e:
            return False
        return True

    def delete_by_email(self, email):
        try:
            user = self.conn.get_collection(
                user_coll).find_one({'email': email})
        except Exception as e:
            return False
        if user is None:
            return user
        try:
            self.conn.get_collection(user_coll).remove({'email': email})
        except Exception as e:
            return False
        return True
