from .app import db


class Belly(db.Model):
    __tablename__ = 'sample_metadata'

    sample = db.Column(db.Integer, primary_key=True)
    EVENT = db.Column(db.String(200))
    ETHNICITY = db.Column(db.String(100))
    GENDER = db.Column(db.String(2))
    AGE = db.Column(db.Float)
    LOCATION = db.Column(db.String(100))
    BBTYPE = db.Column(db.String(2))
    WFREQ = db.Column(db.Float)
    

    __tablename__ = "sample"

    otu_id = db.Column(db.Integer, primary_key=True)
    otu_label = db.Column(db.String(100))
    sample = db.Column(db.Integer, foreign_key = True)
