#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-09 16:39:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nssc!@#$%^&*()'
    SECURITY_PASSWORD_SALT = os.environ.get(
        'SECURITY_PASSWORD_SALT') or 'nssc!@#$%^&*()'

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 465)
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

    MAIL_DEFAULT_SENDER = 'python_api@163.com'

    MAIL_USERNAME = 'python_api@163.com'
    MAIL_PASSWORD = 'python123'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    DEBUG = True


class Production(Config):
    Debug = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": Production,

    "default": DevelopmentConfig
}
