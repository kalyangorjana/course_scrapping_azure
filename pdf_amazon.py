from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import Course_Logger
import course_details
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
import boto3

class pdf_amazon:
    def __init__(self):
        self.course_details = course_details.course_details()

    pdf = canvas.Canvas('data1.pdf')
    def save_pdf_into_amazon_s3(self):
        course_list = self.course_details.get_list_of_courses()[0:20]
        pdf = canvas.Canvas('data.pdf')
        # Create a page for each JSON object and add it to the PDF
        try:
            for course_data in course_list:
                i = 11
                data = json.loads(self.course_details.get_selected_course(course_data.replace(" ",'-')))
                # Add title
                pdf.setFont('Helvetica-Bold', 14)
                pdf.drawString(inch, i * inch, data['title'])

                # Add pricing
                pdf.setFont('Helvetica', 12)
                pdf.drawString(inch, (i-0.6) * inch, 'Pricing')
                pdf.setFont('Helvetica', 11)
                pdf.drawString(1.5 * inch, (i-0.8) * inch, 'IN: ' + str(data['pricing']['IN']))
                pdf.drawString(1.5 * inch, (i-1) * inch, 'US: ' + str(data['pricing']['US']))
                pdf.drawString(1.5 * inch, (i-1.2) * inch, 'Discount: ' + str(data['pricing']['discount']))

                # Add language
                pdf.setFont('Helvetica', 12)
                pdf.drawString(inch, (i-1.8) * inch, 'Language: ' + data['language'])

                # Add requirements
                pdf.setFont('Helvetica', 12)
                pdf.drawString(inch, (i-2.4) * inch, 'Requirements')
                pdf.setFont('Helvetica', 11)
                y = (i-2.6) * inch
                for requirement in data['requirements']:
                    pdf.drawString(1.5 * inch, y, requirement)
                    y -= 0.2 * inch

                # Add course features
                pdf.setFont('Helvetica', 12)
                pdf.drawString(inch, (i - 4) * inch, 'Course Features')
                pdf.setFont('Helvetica', 10)
                y = (i-4.2) * inch
                for feature in data['course_features']:
                    pdf.drawString(1.5 * inch, y, feature)
                    y -= 0.2 * inch
                pdf.showPage()
        except Exception as e:
            Course_Logger(message=str(e))
        self.logger.log(" Data inserted into PDF Successfully ")
        pdf.save()

        try:
            s3 = boto3.client("s3")
            s3.upload_file(
                Filename="data1.pdf",
                Bucket="gk-pdf-bucket",
                Key="gk_user_credentials.csv",
            )
        except Exception as e:
            Course_Logger(message=str(e))
        self.logger.log(" PDF inserted into AWS bucket Successfully ")
        
