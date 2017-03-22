from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

#*** Configure to run locally ***#
# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
# DBS_NAME = 'donorsUSA'
# COLLECTION_NAME = 'projects'
#*** END: Configure to run locally ***#

#* Congfigure to run on heroku *#
MONGODB_URI = os.getenv('MONGODB_URI')
DBS_NAME = os.getenv('MONGO_DB_NAME', 'donorsUS')
COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME', 'projects')
#* END Congfigure to run on heroku *#


FIELDS = {'funding_status': True, 'school_state': True, 'resource_type': True, 'poverty_level': True,
          'date_posted': True, 'total_donations': True, 'primary_focus_area': True, '_id': False}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/donorsUS/projects")
def donor_projects():
    # *** Configure to run locally ***#
    # connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    # *** END: Configure to run locally ***#

    # * Congfigure to run on heroku *#
    connection = MongoClient(MONGODB_URI)
    # * END Congfigure to run on heroku *#
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=55000)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects)
    connection.close()
    return json_projects
#   important to close the connection


if __name__ == "__main__":
    app.run(debug=True)