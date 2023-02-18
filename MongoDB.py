from flask import Flask, render_template, request, jsonify
import json
import course_details
import pymongo
import Course_Logger
import course_details


class MongoDB:
    def __init__(self):
        self.course_details = course_details.course_details()
        self.logger = Course_Logger.Course_Logger()

    def connection(self):
        """To build connection"""
        try:
            client = pymongo.MongoClient(
                "mongodb+srv://kalyan:Kalyan123@cluster1.itvkeub.mongodb.net/?retryWrites=true&w=majority")
            db = client.test
            self.logger.log("Mongo DB Connected Successfully ")
        except Exception as e:
            Course_Logger(message=str(e))
        return client

    def insert_data(self):
        """To insert data into the db"""
        client = self.connection()
        db = client["ineuron_corses"]
        coll = db["course_data"]
        course_list = self.course_details.get_list_of_courses()[0:100]
        try:
            for course_data in course_list:
                data = json.loads(self.course_details.get_selected_course(
                    course_data.replace(" ", '-')))
                coll.insert_one(data)
            self.logger.log(" Data inserted into Mongo DB Successfully ")
        except Exception as e:
            Course_Logger(message=str(e))
        