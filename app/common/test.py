#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-09 18:13:37
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import pymongo
from pymongo import MongoReplicaSetClient
import time
from email import send_email

try:
    conn = MongoReplicaSetClient('39.105.15.174:27020',
                                       replicaSet='rs0', readPreference='secondaryPreferred')
except:
    print 'xxx'
    time.sleep(3)

db = conn['test']
coll = db['test']
j = 0
to = '528762404@qq.com'
subject = "mongodb-replication failed"
message = current_primary + "downd , Please fix up it"

current_primary = conn.primary
while 1:
    try:
        coll.insert_one({'num': j})
        j += 1
        print j
        now_primary = conn.primary
        if current_primary != now_primary:
            send_email(to,subject.message)
    except Exception, e:
        print 'err: ', e
    time.sleep(4.0)