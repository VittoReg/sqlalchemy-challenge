# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    # Create a dictionary with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # Unravel results into a one-dimensional array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    # Unravel results into a one-dimensional array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        # Calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).filter(Measurement.date >= start).all()
        # Unravel results into a one-dimensional array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)
    # Calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Unravel results into a one-dimensional array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run()