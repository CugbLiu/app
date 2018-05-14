#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-09 17:33:34
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import json
import sys
import bcrypt
from . import userApi
from flask import request, g, session, jsonify, current_app, render_template, url_for, redirect
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from authentication import auth
from app.common.email import send_email
from app.common.user_model import User

from settings import my_params

# confirm_ip = 'http://172.25.88.5:5000'
# login_url = 'http://172.25.88.10:8000/login.html'
# reset_url = 'http://172.25.88.10:8000/reset.html'
confirm_ip = my_params.confirm_ip
login_url = my_params.login_url
reset_url = my_params.reset_url

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
@cross_origin()
@userApi.route('/test')
def test():
    return 'xxxxxxxxxxxxxxxx'

@cross_origin()
@userApi.route('/login', methods=['GET', 'POST'])
def login():
    db = getattr(g, 'USER_DB', None)
    email = request.form.get('email', None)
    if email is None:
        return jsonify({'result': 'error', 'message': 'The email can not be empty.'})

    password = request.form.get('password', None)
    if password is None:
        return jsonify({'result': 'error', 'message': 'The password can not be empty.'})

    u = db.query_by_email(email)
    if u == False:
        return jsonify({"error": "background database service error."}), 503
    elif u is None:
        return jsonify({'result': "error", 'message': 'The email does not exist.'})
    else:
        user = User(u['username'], u['email'],
                    u['password'], u['confirmed'])
        tmp = user
        if not user.verify_password(str(password)):
            return jsonify({'result': 'error', 'message': 'Wrong Password.'})
        else:
            if user.confirmed:
                user_token = user.generate_auth_token(expiration=3600)
            else:
                return jsonify({'result': 'error', 'message': 'Incorrect authentication credentials.'})
    g.current_user = user
    session['login_info'] = {
        "username": user.username,
        "sid": user_token
    }
    return jsonify({'result': "success", 'username': user.username, 'token': user_token})


@cross_origin()
@userApi.route("/logout", methods=['GET'])
@auth.login_required
def logout():
    if session.has_key("login_info"):
        username = session['login_info']['username']
        try:
            g.current_user = None
            session.pop("login_info")
        except Exception as e:
            return jsonify({"error": "Logout failed."}), 500
        return jsonify({"error": None, "message": "Logout success."})
    else:
        return jsonify({"error": "Session key does not exist."})


@cross_origin()
@userApi.route('/register', methods=['GET', 'POST'])
def register():
    db = getattr(g, 'USER_DB', None)

    username = request.form.get('username', None)
    if username is None:
        return jsonify({'error': 'username can not be empty.'})

    email = request.form.get('email', None)
    if email is None:
        return jsonify({'error': 'email can not be empty.'})

    pwd = request.form.get('password', None)
    if pwd is None:
        return jsonify({'error': 'password can not be empty.'})
    password = bcrypt.hashpw(str(pwd), bcrypt.gensalt())

    u = db.query_by_email(email)
    if u == False:
        return jsonify({"error": "background database service error."}), 503
    elif u != None:
        return jsonify({'error': email + ' already exists.'})

    user = User(username, email, password)
    token = user.generate_confirmation_token()

    # need modify
    confirm_url = confirm_ip + url_for('registerApi.confirm_email',
                                       token=token, _external=False)

    temp = render_template(
        'activate.html', confirm_url=confirm_url, username=user.username)
    subject = "Please confirm your email address"

    if send_email(user.email, subject, temp):
        if db.insert_user(user):
            return jsonify({'result': 'success', 'username': user.username})
        else:
            return jsonify({'result': 'error', 'message': 'register faliled'}), 500
    else:
        return jsonify({'result': 'error', 'mssage': 'Email sending failed'}), 500


@cross_origin()
@userApi.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = User.confirm(token)
    except:
        return jsonify({'result': 'error', 'message': 'The confirmation link is invalid or has expired.'})
    u = db.query_by_email(email)
    if u == False:
        return jsonify({"error": "background database service error."}), 503
    elif u != None:
        user = User(u['username'], u['email'], u['password'], u['confirmed'])
        if user.confirmed:
            # need modify
            return redirect(login_url)
        else:
            user.confirmed = True
            db.update_user_confirmed(email, user.confirmed)
            # need modify
            return redirect(login_url)
    else:
        return jsonify({'result': 'error', 'message': 'Confirm error.'})


@cross_origin()
@userApi.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    email = request.values.get('email', None)
    if email is None:
        return jsonify({'result': 'error', 'message': "Email can't be empty."})
    else:
        u = db.query_by_email(email)
        # print '-----------------------------------'
        # print u, email
        # print '-----------------------------------'
        if u == False:
            return jsonify({"error": "background database service error."}), 503
        elif u is None:
            return jsonify({'result': 'error', 'message': "Sorry, can't find the user."})

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'reset_email': email})

        # need modify reset_url
        temp = render_template(
            'reset.html', reset_url=reset_url + '?token=' + token, username=user.username)

        subject = "Reset your password"
        if send_email(email, subject, temp):
            return jsonify({'result': 'success', 'message': 'We have sent you an email with instructions to reset your password.'})
        else:
            return jsonify({'result': 'error', 'message': 'Email sending failed'})


@cross_origin()
@userApi.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    db = getattr(g, 'USER_DB', None)

    password = request.form.get('password', None)
    if password is None:
        return jsonify({'result': 'error', 'message': 'Password cannot be empty.'})

    confirm_password = request.form.get('confirm_password', None)
    if confirm_password is None:
        return jsonify({'result': 'error', 'message': 'Confirm password cannot be empty.'})
    elif confirm_password != password:
        return jsonify({'result': 'error', 'message': 'Confirm password is not the same as password.'})

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return jsonify({'result': 'error', 'message': 'The token is invalid or has expired.'})
    if data is not None:
        email = data.get('reset_email', None)
        if email is None:
            return jsonify({'result': 'error', 'message': 'The token is invalid or has expired.'})
        else:
            u = db.query_by_email(email)
            if u == False:
                return jsonify({"error": "background database service error."}), 503
            elif u is None:
                return jsonify({'result': 'error', 'message': "Sorry, cannot find the email. \
                    The token maybe is invalid or expired, please request again."})
            else:
                try:
                    if db.reset_user_password(email, password, confirmed=True):
                        return redirect(login_url)
                    else:
                        return jsonify({'result': 'error', 'message': "Reset password failed."})
                except Exception as e:
                    return jsonify({'result': 'error', 'message': "Reset password failed."})
