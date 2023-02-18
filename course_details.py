from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import Course_Logger

class course_details:
    def __init__(self):
        self.details = {}
        self.courses_list = []
        self.ineuron_url = 'https://ineuron.ai/courses'
        self.logger = Course_Logger.Course_Logger()

    def get_list_of_courses(self):
        self.logger.log(f"searching for url {self.ineuron_url}")
        url_response = uReq(self.ineuron_url)
        ineuron_page = url_response.read()
        self.logger.log(f"Successfully got respose for the url {self.ineuron_url}")
        url_response.close()
        ineuron_html = bs(ineuron_page, 'html.parser')
        course_data = json.loads(ineuron_html.find('script', id = "__NEXT_DATA__").get_text())
        all_courses = course_data['props']['pageProps']['initialState']['init']['courses']
        self.logger.log("Successfully got the all courses..")
        self.courses_list = list(all_courses.keys())
        self.logger.log("Sending the all courses keys..")
        return self.courses_list
    
    def get_selected_course(self,course):
        self.logger.log("searching for selected course form all courses....")
        course_url = self.ineuron_url[0:len(self.ineuron_url)-1] + "/"+ course
        url_response = uReq(course_url)
        course_page = url_response.read()
        self.logger.log(f"Successfully got respose for the url {course_url}")
        url_response.close()
        course_html = bs(course_page, 'html.parser')
        course_data = json.loads(course_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
        self.logger.log(f"Successfully got respose as text for the url {course_url}")
        return self.add_details(course_data,course_url)

    def add_details(self,course_data,course_url):
        self.logger.log("getting data from the respose")
        try:
            # To get the course title
            self.details["title"] = course_data['props']['pageProps']['data']['title']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
            # To get description
            self.details["description"] = course_data['props']['pageProps']['data']['details']['description']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

            
        try:
            # To get class detials
            self.details["class_details"] = course_data['props']['pageProps']['data']['details']['classTimings']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
            # To get the pricing
            self.details["pricing"] = course_data['props']['pageProps']['data']['details']['pricing']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
            # To get course features
            self.details["course_features"] = course_data['props']['pageProps']['data']['meta']['overview']['features']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
            # To get the what you learn data
            self.details["learn"] = course_data['props']['pageProps']['data']['meta']['overview']['learn']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
            # To get the requriements
            self.details['requirements'] = course_data['props']['pageProps']['data']['meta']['overview']['requirements']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
             # To get the language
            self.details["language"] = course_data['props']['pageProps']['data']['meta']['overview']['language']
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)
        
        try:
             # To get the curriculum
            curriculum = []
            keylist = list((course_data['props']['pageProps']['data']['meta']['curriculum']).keys())
            for i in keylist:
                curriculum.append(course_data['props']['pageProps']['data']['meta']['curriculum'][i]['title'])
            self.details["curriculum"] = curriculum
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)

        try:
            # To get instructors
            all_instructors = course_data['props']['pageProps']['initialState']['init']['instructors']
            assigned_instructors = course_data['props']['pageProps']['data']['meta']['instructors']
            i_li = []
            for i in assigned_instructors:
                i_li.append(all_instructors[i])
            self.details["instructors"] = i_li
        except Exception as e:
            Course_Logger(message=str(e), src=course_url)
        
        return json.dumps(self.details)