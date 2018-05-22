# import necessary libraries
import numpy as np
import DataExploration
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
     redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine



# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)


# Create database tables
@app.before_first_request
def setup():
  
    db.create_all()

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    
@app.route('/names')
def names():
    SampleNames = DataExploration.SampleNames()
    print(SampleNames)
    return jsonify(SampleNames)
   
@app.route('/otu')

def otuDef():
    return jsonify( {
            "x": [1,2],
            "y": [2,4]
            
    })