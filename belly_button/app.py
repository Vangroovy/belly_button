import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
#app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)
#from .models import Sample
#from .models import SampleMetadata

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)
Samples = Base.classes.samples
Samples_Metadata = Base.classes.sample_metadata

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""

    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["SAMPLE"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    return jsonify(sample_metadata)


@app.route("/scattersamples/<sample>")
def scattersamples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""

    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    
    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist()
    }
    return jsonify(data)

@app.route("/piesamples/<sample>")  
def piesamples(sample): 
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    
    # Filter the data based on the sample number and
    # only keep rows with values above 1
    # retrieve the top 10 sample_data
    pie_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    pie_data = pie_data.sort_values(sample, ascending=False).head(10)

    # Format the data to send as a json
    sorted_list = {
        "otu_ids": pie_data.otu_id.values.tolist(),
        "sample_values": pie_data[sample].values.tolist(),
        "otu_labels": pie_data.otu_label.tolist()
    }
    return jsonify(sorted_list)

if __name__ == "__main__":
    app.run()
