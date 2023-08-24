# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    '''List all available routes'''
    return(
        f"<h1>Available Routes:</h1><br/>"
        f'<a href="http://127.0.0.1:5000/api/v1.0/precipitation"><b>/api/v1.0/precipitation</b></a><br/>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/stations"><b>/api/v1.0/stations</b></a><br/>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/tobs"><b>/api/v1.0/tobs</b></a><br/>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/2017-08-01"><b>/api/v1.0/&lt;start_date(YYYY-MM-DD)&gt;</b><br/>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/2016-08-01/2017-01-01"><b>/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;</b><br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=(dt.date(2016, 8, 23))).all()
    session.close()
    
    prcp_list=[]
    for date, prcp in results:
        prcp_dict={}
        prcp_dict['date']= date
        prcp_dict['prcp']= prcp
        prcp_list.append(prcp_dict)
    
    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results= session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=(dt.date(2016, 8, 23)))\
            .filter(Measurement.station=='USC00519281').all()
    session.close()

    tobs_list=[]
    for date, tobs in results:
        tobs_dict={}
        tobs_dict['date']= date
        tobs_dict['tobs']= tobs
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/")
def start(start):
    results=session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date>=start).all()
    session.close()

    start_list=[]
    for tmax, tmin, tavg in results:
        start_dict={}
        start_dict['max']= tmax
        start_dict['min']= tmin
        start_dict['avg']= tavg
        start_list.append(start_dict)

    return jsonify(start_list)


@app.route("/api/v1.0/<start>/<end>/")
def time(start,end):
    session= Session(engine)
    results=session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()

    time_list=[]
    for tmax, tmin, tavg in results:
        time_dict={}
        time_dict['max']= tmax
        time_dict['min']= tmin
        time_dict['avg']= tavg
        time_list.append(time_dict)

    return jsonify(time_list)



if __name__ == '__main__':
    app.run(debug=True)