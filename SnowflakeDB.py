from flask import Flask, render_template, request, jsonify
import json
import Course_Logger
import course_details
import snowflake.connector
import re


class SnowflakeDB():
    def __init__(self):
        self.course_details = course_details.course_details()

    def insert_data(self):
        course_list = self.course_details.get_list_of_courses()
        # Connecting to Snowflake using default authenticator
        try:
            con = snowflake.connector.connect(
                user='root',
                password='Kalyan@123',
                account='by21058.ap-southeast-1'
            )
            self.logger.log("Connected to Snowflake Successfully ")
        except Exception as e:
            Course_Logger(message=str(e))
        try:
            # Creating a new database
            con.cursor().execute("CREATE DATABASE IF NOT EXISTS Course")
            # Using the database
            con.cursor().execute("USE DATABASE Course")
            self.logger.log("Created Database in Snowflake Successfully ")
        except Exception as e:
            Course_Logger(message=str(e))
        
        try:
            # Creating the table
            con.cursor().execute("CREATE TABLE IF NOT EXISTS Course_data (title VARCHAR,class_details VARCHAR,pricing VARCHAR,course_features VARCHAR,learn VARCHAR,requirements VARCHAR,language VARCHAR,curriculum VARCHAR)")
            self.logger.log("Created table in Snowflake Successfully ")
        except Exception as e:
            Course_Logger(message=str(e))

        try:   
            for course_data in course_list[0:21]:
                data = json.loads(self.course_details.get_selected_course(course_data.replace(" ",'-')))
                # Storing the data items in variables
                title = data['title']
                class_details = re.sub("\'","\"",str(data['class_details']))
                pricing = re.sub("\'","\"",str(data["pricing"]))
                course_features = re.sub("\'","\"",str(data["course_features"]))
                learn = re.sub("\'","\"",str(data["learn"]))
                requirements = re.sub("\'","\"",str(data["requirements"]))
                language = re.sub("\'","\"",str(data["language"]))
                curriculum = re.sub("\'","\"",str(data["curriculum"]))
                # Creating the insert statement
                con.cursor().execute(f"INSERT INTO Course_data VALUES('{title}','{class_details}','{pricing}','{course_features}','{learn}','{requirements}','{language}','{curriculum}')")
        except Exception as e:
            Course_Logger(message=str(e))
        # Committing the changes
        con.commit()
        self.logger.log("Data inserted into Snowflake Successfully ")
        # Closing the connection
        con.close()
