# IneuronCourseScrappingWebsite-Public
Developed project with intention of understanding of web scrapping, flask-api integration.

This project provides an overview of how to implement Webscrapping using python.

**Introduction of Webscrapping:** Web scrapping is extracting data from a website and creating our own analysis on it.

<ul>
<li>app.py is the core api layer which accepts request and return a response a file</li>
  <li>Operations:
    <ul>
      <li>"/" : Redirects to home screen where you can select the course</li>
      <li>"/course_details" : Redirects to selected code details</li>
    </ul>
  </li>
  <li>course_deatils.py which extract the data form the ineuron website</li>
  <li>pdf_amazon.py, MongoDB.py, SnowflakeDB.py are the database related connection setting and operations</li>
  <li>Course_Logger.py is logging files</li>
  <li>requirements.txt is the application package related information file</li>
</ul>

<h2>Libraries used</h2>
<ul>
<li>requests</li>
<li>bs4</li>
<li>flask</li>
<li>requests_html</li>
<li>boto3</li>
<li>pymongo</li>
<li>snowflake-connector-python</li>
<li>reportlab</li>
</ul>