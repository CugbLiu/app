#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-13 19:15:32
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from flask import Flask
from config import config
from flask_mail import Mail
from flask_cors import CORS
from pymongo import MongoClient,MongoReplicaSetClient
import time

mail = Mail()
from settings import my_params
user_mongo_url = my_params.user_mongo_url
user_mongo_port = my_params.user_mongo_port

data_mongo_url = my_params.data_mongo_url
data_mongo_port = my_params.data_mongo_port
# from app.common.email import send_email
user_db = MongoReplicaSetClient(user_mongo_url+":"+str(user_mongo_port),
                                replicaSet='rs0', readPreference='secondaryPreferred')


# user_db = MongoClient(user_mongo_url,user_mongo_port)
data_db = MongoClient(data_mongo_url,data_mongo_port)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from api_1_0 import istpApi as istpApi_1_0
    from api_1_0 import iagaApi as iagaApi_1_0
    from api_1_0 import userApi as userApi_1_0
    app.register_blueprint(istpApi_1_0, url_prefix='/api/v1.0/istp')
    app.register_blueprint(userApi_1_0, url_prefix='/api/v1.0/auth')
    app.register_blueprint(iagaApi_1_0, url_prefix='/api/v1.0/iaga')

    mail.init_app(app)
    CORS(app)

    return app
