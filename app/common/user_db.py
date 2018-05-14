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
from email import send_email

# user_db = 'USER'
# user_coll = 'user'
user_db_1 = my_params.user_db
user_coll = my_params.user_coll
current_primary = None
to = my_params.administor_emial
subject = my_params.administor_subject
first = 1
class USER_DB:
    def __init__(self):
        global current_primary
        global first
        now_primary = user_db.primary
        if first == 1:
            current_primary = now_primary
            first = 2
        print '*****************'
        print 'current_primary:',current_primary
        print 'now_primary',now_primary
        print '*****************'
        html = "The " + str(current_primary) + " had failed , Please fixed up it quickly"
        if now_primary != None:
            if now_primary != current_primary:
                print 'send email...'
                current_primary = now_primary
                send_email(to,subject,html)
                time.sleep(5)
        self.conn = user_db[user_db_1]

    def query_by_email(self, email):
        try:
            result = self.conn.get_collection(user_coll).find_one({'email': email})
            return result
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
