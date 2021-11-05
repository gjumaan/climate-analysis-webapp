#Import dependencies
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

# Save re-usable variables
one_year_from_last = dt.date(2017,8,23) - dt.timedelta(days=365)
temps = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using date as the key and prcp as the value
    # Return the JSON representation of your dictionary
    prcp_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_from_last).\
        order_by(measurement.date).all()
    
    session.close()

    prcp_data_list = dict(prcp_data)
    
    return prcp_data_list

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset
    total_stations = session.query(station.station, station.name).all()

    session.close()

    total_stations_list = dict(total_stations)

    return total_stations_list

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data
    # Return a JSON list of temperature observations (TOBS) for the previous year
    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= one_year_from_last).\
        filter(measurement.station == 'USC00519281').\
        order_by(measurement.date).all()
    
    session.close()

    tobs_data_list = dict(tobs_data)

    return tobs_data_list

def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    start_data = session.query(*temps).\
        filter(measurement.date >= start).all()

    session.close()

    start_data_list = list(np.ravel(start_data))

    return start_data_list

def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    start_end_data = session.query(*temps).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    session.close()

    start_end_data_list = list(np.ravel(start_end_data))

    return start_end_data_list