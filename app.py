# import necessary libraries
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func
from flask_sqlalchemy import SQLAlchemy

import pandas as pd
import numpy as np

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
# Database Queries Setup
#################################################

#db = SQLAlchemy(app)

# Create engine using 
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/names')
def SampleNames():
    #Query the Samples
    results = engine.execute('SELECT* FROM samples LIMIT 1')

    for row in results:
        colnames = (row.keys())
        
    sampleList = [k for k in colnames]
    print(sampleList[1:])

    return jsonify(sampleList[1:])
   
@app.route('/otu')
def otuDef():
    OtuResults = session.query(Otu.lowest_taxonomic_unit_found).all()
    OtuDf = pd.DataFrame(OtuResults)
    OtuDf = OtuDf.rename(columns={"lowest_taxonomic_unit_found": "OtuDesc"})
    OtuList = OtuDf['OtuDesc'].tolist()
    return jsonify(OtuList)

@app.route('/metadata/<sample>')
def sampleMeta(sample):
    #sample = "BB_940"
    sampleID = sample.replace("BB_","")
    sampleMetaData = session.query(Samples_Metadata.AGE,Samples_Metadata.BBTYPE,\
                               Samples_Metadata.ETHNICITY,Samples_Metadata.GENDER,\
                               Samples_Metadata.LOCATION,Samples_Metadata.SAMPLEID).\
                               filter(Samples_Metadata.SAMPLEID == sampleID).all()
    sampleMetaDataDF = pd.DataFrame(sampleMetaData)
    sampleIDDict = sampleMetaDataDF.to_dict('records')
    
    return jsonify(sampleIDDict)

@app.route('/wfreq/<sample>')
def washFreq(sample):
#    sample = "BB_940"
    sampleID = sample.replace("BB_","")
    washFreqResult = session.query(Samples_Metadata.WFREQ).\
                               filter(Samples_Metadata.SAMPLEID == sampleID).first()
    print(washFreqResult[0])
    return jsonify(washFreqResult)
 
@app.route('/samples/<sample>')
def sampleData(sample): 
    
    #sampleID = "BB_940"
    #Reading the samples table into a dataframe
    results = engine.execute('SELECT* FROM samples')
    Sampledf = pd.DataFrame(results.fetchall())
    Sampledf.columns = results.keys()  
    Sampledf = Sampledf[["otu_id",sample]]
    Sampledf = Sampledf.loc[Sampledf[sample] > 0]
    Sampledf = Sampledf.sort_values(by=sample, ascending=False)
    Sampledf = Sampledf.rename(columns={"sample": "sample_values", "otu_id": "otu_ids" })
    SampleDict = Sampledf.to_dict('list')
    print(SampleDict) 
    return jsonify(SampleDict)
 
if __name__ == "__main__":
    app.run(debug=True)