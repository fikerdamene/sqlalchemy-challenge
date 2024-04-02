# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)
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

# Home Page
@app.route("/")
def home():
    """Homepage - List all available api routes."""
    print("Request to homepage made...")
    return (
        f"Available Routes:<br/>"
        "<br/>"
        f"Static Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "<br/>"
        f"Dynamic Routes:<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

#----------------------------------------------------#
# Precipitation Page
@app.route("/api/v1.0/precipitation")
def precip():
    """Query 12 Months of Precipitation data - Return as JSON"""
    print("Request to Precipitation data made...")
    session

    annum_prcp = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= dt.date(2016,8,23)).order_by(Measurement.date.desc()).all()

    session.close()

    # Convert results to a dictionary
    precip_annual = []
    for date, prcp in annum_prcp:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_annual.append(precip_dict)
    
    # JSONify the precip_annual list
    return jsonify(precip_annual)

#----------------------------------------------------#
# Stations Page
@app.route("/api/v1.0/stations")
def stations():
    """Query a list of stations - Return as JSON"""
    print("Request to Station list data made...")
    session

    stations = session.query(Station).all()

    session.close()

    # Convert results to a dictionary
    station_list = []
    for station in stations:
        main_dict = {}
        main_dict['Station'] = station.station
        main_dict['Station_Details'] = {
            "ID":station.id,
            "Name":station.name,
            "Latitude":station.latitude,
            "Longitude":station.longitude,
            "Elevation":station.elevation
        }
        station_list.append(main_dict)
    
    # JSONify the Station_list list
    return jsonify(station_list)

#----------------------------------------------------#
# Tobs Page
@app.route("/api/v1.0/tobs")
def tobs():
    """Query a most active station - Return tobs as JSON"""
    print("Request for tobs of most active station made...")
    session

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= dt.date(2016,8,18)).all()

    session.close()

    # Convert results to a dictionary
    tobs_list = []
    for date, tobs in tobs:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Temperature'] = tobs
        tobs_list.append(tobs_dict)

    # JSONify the tobs_list list
    return jsonify(tobs_list)    

#----------------------------------------------------#
# Dynamic Page - Start Date only
@app.route("/api/v1.0/<start>")
def dynamic_1(start):
    """Dynamic query to retrieve data from the given start date - Min, Max, Avg Temp as JSON"""
    print("Request for data with a start date given...")

    # Convert start to date format
    try:
        # If the date given by the user contains "-" between Year, Month, Day - Remove the character
        if (start.__contains__("-")):
            start = start.replace("-","")
        
        s_date = dt.datetime.strptime(start, '%Y%m%d')

        session

        # Variables for reference to temperature calculations
        tmin = func.min(Measurement.tobs)
        tmax = func.max(Measurement.tobs)
        tavg = func.avg(Measurement.tobs)

        data_request = session.query(tmin,tmax,tavg).filter(Measurement.date >= s_date).all()

        session.close()

        temp_data = []
        for tmin, tmax, tavg in data_request:
            temp_dict = {}
            temp_dict['From_Date'] = start
            temp_dict['Temp_Calcs'] = {
                "Min Temperature" : tmin,
                "Max Temperature" : tmax,
                "Avg Temperature" : round(tavg,2)
            }
            temp_data.append(temp_dict)

        # JSONify the temp_data list
        return jsonify(temp_data)
    
    # Exception handle if date given is in the incorrect format
    except ValueError:
        return jsonify({"error": f"The specified date '{start}' is not in the correct format.",
                        "note": f"Place a date in the format: yyyy-mm-dd or yyyymmdd"}), 404

#----------------------------------------------------#
# Dynamic Page - Start and End date
@app.route("/api/v1.0/<start>/<end>")
def dynamic_2(start,end):
    """Dynamic query to retrieve data from the given start date to given end date - Min, Max, Avg Temp as JSON"""
    print("Request for data with a start date and end date given...")

    # Convert start to date format
    try:
        # If the date given by the user contains "-" between Year, Month, Day - Remove the character
        if (start.__contains__("-")) or (end.__contains__("-")):
            start = start.replace("-","")
            end = end.replace("-","")

        s_date = dt.datetime.strptime(start, '%Y%m%d')
        e_date = dt.datetime.strptime(end, '%Y%m%d')

        # Check if the end date given is greater than the start date
        if (e_date > s_date):

            session

            # Variables for reference to temperature calculations
            tmin = func.min(Measurement.tobs)
            tmax = func.max(Measurement.tobs)
            tavg = func.avg(Measurement.tobs)

            data_request = session.query(tmin,tmax,tavg).filter(Measurement.date >= s_date).filter(Measurement.date <= e_date).all()

            session.close()

            temp_data = []
            for tmin, tmax, tavg in data_request:
                temp_dict = {}
                temp_dict['From_Date'] = start
                temp_dict['To_Date'] = end
                temp_dict['Temp_Calcs'] = {
                    "Min Temperature" : tmin,
                    "Max Temperature" : tmax,
                    "Avg Temperature" : round(tavg,2)
                }
                temp_data.append(temp_dict)

            # JSONify the temp_data list
            return jsonify(temp_data)
        
        # If the end date is less than start date, return an error and prompt for dates to be changed
        else:
            return jsonify({"error":f"The end date '{end}' can not be less than the start date '{start}'. Please adjust your date values."}), 404
    
    # Exception handle if date given is in the incorrect format
    except ValueError:
        return jsonify({"error": f"One of the specified dates '{start}' or '{end}' is not in the correct format.",
                        "note": f"Alter the dates to the format: yyyy-mm-dd or yyyymmdd"}), 404


if __name__ == '__main__':
    app.run(debug=False)