#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-24 10:38:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from flask_mail import Message
from flask import current_app
from app import mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    # print '--------------------------------------------'
    # print current_app.config['MAIL_DEFAULT_SENDER']
    # print '--------------------------------------------'
    try:
        mail.send(msg)
    except Exception as e:
        return False
    return True
