#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-09 16:39:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
class myParmas:
    def __init__(self):
        # self.user_mongo_url = os.environ.get('DB_NAME')
        self.user_mongo_url = '39.105.15.174'
        self.user_mongo_port = 27022
        self.current_primary = self.user_mongo_url + str(self.user_mongo_port)
        self.data_mongo_url = '39.105.15.174'
        self.data_mongo_port = 27018
        self.user_db = 'USER'
        self.user_coll = 'user'

        self.istp_db = "ISTP_1"
        self.ispt_attrs = 'attrs'
        self.istp_data = 'data'

        self.iaga_db = "IAGA_Release"
        self.iaga_data = 'data'
        self.iaga_header = 'files'
        self.iaga_station = 'stations'

        self.administor_emial = '528762404@qq.com'
        self.administor_subject = 'mongodb replication failed'

        self.confirm_ip = 'http://39.105.15.174:5001/api/v1.0/auth'
        self.login_url = 'http://172.20.64.184:80/app/login.html'
        self.reset_url = 'http://172.20.64.184:80/app/reset.html'

my_params = myParmas()

