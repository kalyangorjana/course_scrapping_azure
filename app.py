from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import course_details
import pdf_amazon
import MongoDB
import SnowflakeDB

app = Flask(__name__)
course = course_details.course_details()
pdf = pdf_amazon.pdf_amazon()
mongodb = MongoDB.MongoDB()
snowflake = SnowflakeDB.SnowflakeDB()

@app.route("/")
def hello_world():
    course_namelist = course.get_list_of_courses()
    # pdf.save_pdf_into_amazon_s3()
    # mongodb.insert_data()
    # snowflake.insert_data()
    return render_template('index.html', myList=course_namelist)

@app.route('/course_details', methods=['POST'])
def index():
    if request.method == 'POST':
        selected_item = request.form.get('list')
        course_details = course.get_selected_course(selected_item.replace(" ","-"))
    return render_template("result.html",json_data = json.loads(course_details))

@app.errorhandler(404)
def error_page(e):
    return render_template(
        'error.html',
        exception_type="Page not found",
        exception_title=str(e),
        exception_message="Sorry, an error has occurred, Requested page not found!",
        breadcrum=f"/Error"
    )

@app.errorhandler(500)
def error_page(e):
    return render_template(
        'error.html',
        exception_type="Internal server error",
        exception_title=str(e),
        exception_message="Sorry, an internal error has occurred, try again!",
        breadcrum=f"/Error"
    )


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5003)
