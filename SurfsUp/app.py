from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from flask_cors import CORS
import datetime as dt
import pandas as pd

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;</br>"
    )

@app.route("/api/v1.0/precipitation")
def precip_json():
    # Return JSON dictionary of last 12 months of precipitation data
    session = Session(engine)
    last_row = session.query(measurement).order_by(measurement.date.desc()).first()
    last_date = last_row.date
    first_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    prcp_data = session.query(measurement.date,measurement.prcp).filter(measurement.date > first_date).all()
    session.close()
    prcp_df = pd.DataFrame(prcp_data)
    cleaned_prcp_df = prcp_df.dropna()
    cleaned_prcp_df.sort_values('date',axis=0)
    precip_dict = dict(zip(cleaned_prcp_df['date'],cleaned_prcp_df['prcp']))
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations_json():
    # Return a JSON list of stations
    session = Session(engine)
    stations_data = session.query(station.station).all()
    session.close()
    stations_list = list(stations_data)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs_json():
    # Returns JSONified data of temperature observations from the previous year at most active station
    session = Session(engine)
    last_row = session.query(measurement).order_by(measurement.date.desc()).first()
    last_date = last_row.date
    first_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    tobs_data = session.query(measurement.date, measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date > first_date).all()
    session.close()
    tobs_df = pd.DataFrame(tobs_data)
    tobs_dict = dict(zip(tobs_df['date'],tobs_df['tobs']))
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start_json(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range.
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    session = Session(engine)
    tmin = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).all()
    tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    tmax = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    return jsonify(tmin[0][0],tavg[0][0],tmax[0][0])

@app.route("/api/v1.0/<start>/<end>")
def end_json(start,end):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range.
    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    session = Session(engine)
    tmin = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).\
        filter(end >= measurement.date).all()
    tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).\
        filter(end >= measurement.date).all()
    tmax = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).\
        filter(end >= measurement.date).all()
    session.close()
    return jsonify(tmin[0][0],tavg[0][0],tmax[0][0])




if __name__ == '__main__':
    app.run(debug=True)