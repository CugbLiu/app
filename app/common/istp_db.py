#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-06 10:55:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from app import data_db
from settings import my_params
# istp_db = "ISTP_1"
# ispt_attrs = 'attrs'
# istp_data = 'data'
istp_db = my_params.istp_db
ispt_attrs = my_params.ispt_attrs
istp_data = my_params.istp_data

class ISTP_DB:
    def __init__(self):
        self.conn = data_db[istp_db]

    def get_element_list(self, element, condition=None):
        try:
            return self.conn.get_collection(ispt_attrs).distinct(element, condition)
        except Exception as e:
            return False

    def get_element_and_full_list(self, element, condition=None):
        e_list = ["Project", "Source_name", "Descriptor", "Data_type"]
        if element not in e_list:
            return self.get_element_list(element, condition)
        res = []
        try:
            elem_list = self.conn.get_collection(
                ispt_attrs).distinct(element, condition)
        except Exception as e:
            return False
        for elem in elem_list:
            temp = {}
            temp[element] = elem
            try:
                temp["full_" + element] = self.conn.get_collection(ispt_attrs).distinct(
                    "full_" + element, {
                        "full_" + element: {"$nin": ['', ' ', None]},
                        element: elem
                    })[0]
            except Exception as e:
                return False
            res.append(temp)
        return res

    def get_data_sets(self, condition):
        term = {}
        term["Data_type"] = 1
        term["full_Data_type"] = 1
        try:
            data_sets = list(self.conn.get_collection(
                "attrs").find(condition, term))
        except Exception as e:
            return False
        return data_sets

    def get_variables(self, logical_source, var_type=None):
        condition = {}
        condition["_id"] = logical_source
        try:
            attrs = self.conn.get_collection("attrs").find_one(condition)
        except Exception as e:
            return False
        variables = []
        if attrs != None:
            for key in attrs.keys():
                if isinstance(attrs[key], dict):
                    if var_type != None:
                        if "VAR_TYPE" in attrs[key].keys() and attrs[key]["VAR_TYPE"] == var_type:
                            variables.append(key)
                    else:
                        variables.append(key)
        return sorted(variables)

    def get_attribute(self, logical_source, variables):
        term = {}
        term["_id"] = 0
        var_list = self.get_variables(logical_source, "data")
        if var_list == False:
            return False
        elif var_list == None:
            return {"error": "data_set"}

        for variable in variables:
            if variable in var_list:
                term[variable] = 1

        if len(term.keys()) <= 1:
            return {"error": "variables"}

        try:
            attr = self.conn.get_collection("attrs").find_one(
                {"_id": logical_source}, term)
        except Exception as e:
            return False

        if attr == None:
            return {"error": "data_set"}
        elif attr == {}:
            return {"error": "variables"}

        var_list = self.get_variables(logical_source)
        if var_list == False:
            return False

        for variable in attr.keys():
            for key in attr[variable].values():
                if key in var_list:
                    term[key] = 1

        try:
            attr = self.conn.get_collection("attrs").find_one(
                {"_id": logical_source}, term)
        except Exception as e:
            return False
        return attr

    def get_data(self, logical_source, variables, start_time=None, end_time=None):
        term = {}
        attr = self.get_attribute(logical_source, variables)
        if attr == False:
            return False, []
        elif "error" in attr:
            return attr, []

        for variable in attr.keys():
            term[variable] = 1

        term["_id"] = 0
        term["time_stamp"] = 1
        condition = {}
        condition["Logical_source"] = logical_source

        if start_time != None and end_time != None:
            condition["time_stamp"] = {"$gte": start_time, "$lte": end_time}

        variables = list(set(variables) & set(attr.keys()))
        condition["$or"] = []

        for variable in variables:
            condition["$or"].append({variable: {"$exists": 1}})

        data = self.conn.get_collection(istp_data).find(
            condition, term).sort([('time_stamp', 1)])
        return attr, data
