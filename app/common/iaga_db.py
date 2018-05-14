#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-20 21:11:27
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import time
from app import data_db
from settings import my_params

# iaga_db = "IAGA_Release"
# iaga_data = 'data'
# iaga_header = 'files'
# iaga_station = 'stations'
iaga_db = my_params.iaga_db
iaga_data = my_params.iaga_data
iaga_header = my_params.iaga_header
iaga_station = my_params.iaga_station

class IAGA_DB:
    def __init__(self):
        self.conn = data_db[iaga_db]

    def get_stations(self, start_longitude, end_longitude, start_latitude, end_latitude):
        stations = self.conn.get_collection(iaga_station).find({
            '$and': [
                {'Geodetic Latitude':
                    {'$gte': start_latitude, '$lte': end_latitude}},
                {'Geodetic Longitude':
                    {'$gte': start_longitude, '$lte': end_longitude}}
            ]
        }, {
            '_id': 0, 'Station Name': 1,
            'IAGA CODE': 1,
            'Geodetic Latitude': 1, 'Geodetic Longitude': 1
        }).sort("IAGA CODE", 1)
        return stations

    def get_iaga_codes(self, start_longitude, end_longitude, start_latitude, end_latitude):
        stations = self.conn.get_collection(iaga_station).distinct('IAGA CODE', {
            '$and': [
                {'Geodetic Latitude':
                    {'$gte': start_latitude, '$lte': end_latitude}},
                {'Geodetic Longitude':
                    {'$gte': start_longitude, '$lte': end_longitude}}
            ]
        })
        return stations

    def get_time_range(self, start_time, end_time):
        min_time_stamp = self.conn.get_collection(
            iaga_data).find().sort([("time_stamp", 1)]).limit(1)[0]["time_stamp"]
        max_time_stamp = self.conn.get_collection(
            iaga_data).find().sort([("time_stamp", -1)]).limit(1)[0]["time_stamp"]

        if (start_time is None) or (start_time < min_time_stamp):
            start_time = min_time_stamp
        if (end_time is None) or (end_time > max_time_stamp):
            end_time = max_time_stamp
        return start_time, end_time

    def __getTimeStep(self, time_interval):
        if time_interval <= 1:
            return 1
        elif time_interval <= 3:
            return 5
        elif time_interval <= 6:
            return 15
        elif time_interval <= 12:
            return 30
        elif time_interval <= 24:
            return 60
        elif time_interval <= 72:
            return 120
        elif time_interval <= 168:
            return 300
        elif time_interval <= 360:
            return 600
        elif time_interval <= 720:
            return 900
        elif time_interval <= 1440:
            return 1800
        elif time_interval <= 2880:
            return 3600
        elif time_interval <= 4320:
            return 7200
        elif time_interval <= 8640:
            return 10800
        elif time_interval <= 17280:
            return 21600
        elif time_interval <= 43200:
            return 43200
        elif time_interval <= 86400:
            return 86400
        elif time_interval <= 172800:
            return 172800
        else:
            return 604800

    def get_time_step(self, sample, start_time, end_time):
        time_interval = (end_time - start_time) / 3600
        if "sec" in sample:
            return self.__getTimeStep(time_interval)
        else:
            if time_interval <= 24:
                return 60
            return self.__getTimeStep(time_interval)

    def get_data(self, start_time, end_time, stations, term, sample, data_type):
        query = {}
        # if data add reported, this for loop can remove
        for i in term.keys():
            query[i] = {"$exists": 1}

        query['Type'] = {'$in': data_type}
        query['InterTpye'] = {'$in': sample}
        query['IAGA CODE'] = {'$in': stations}

        start_time, end_time = self.get_time_range(start_time, end_time)
        time_step = self.get_time_step(sample, start_time, end_time)
        time_remainder = start_time % time_step

        query['time_stamp'] = {
            '$gte': start_time, '$lte': end_time, '$mod': [time_step, time_remainder]}

        for key in ['IAGA CODE', 'time_stamp', 'InterTpye', 'Type']:
            term[key] = 1
        term['_id'] = 0

        data = self.conn.get_collection(iaga_data).find(query, term).sort(
            [('time_stamp', 1)])
        return data

    def get_reported(self, stations=None):
        condition = {}
        if stations != None:
            condition = {'IAGA CODE': {'$in': stations}}
        reportde_types = self.conn.get_collection(
            iaga_header).distinct("Reported", condition)
        return reportde_types
