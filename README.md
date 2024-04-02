sqlalchemy-challenge

Hawaii Climate Analysis
________________________________________
Overview:

This project involves analyzing climate data from Hawaii using Python, SQLAlchemy, and Matplotlib. The data is stored in an SQLite database containing two tables: measurement and station. The project performs exploratory analysis on precipitation and temperature data.

Setup Instructions:

To run this project, these steps are followed:
•	Installed Python and necessary libraries (matplotlib, pandas, sqlalchemy).

•	Cloned or downloaded the project repository from GitHub.

•	Ensured the SQLite database hawaii.sqlite is located in the specified directory.

•	Run the provided Python script in my preferred environment.

Dependencies:

Python 3.x

Matplotlib

Pandas

SQLAlchemy

File Structure:

README.md: Documentation for the project.

climate_analysis.py: Python script containing the code for data analysis.

hawaii.sqlite: SQLite database containing climate data for Hawaii.

Exploratory Analysis:

1. Precipitation Analysis:
- Retrieved the most recent date in the dataset.

- Query and plotted the precipitation data for the last 12 months.

- Calculated summary statistics for precipitation.
- 
2. Station Analysis:

- Calculated the total number of stations.

- Determined the most active station and its observations.

- Retrieved and plotted the temperature observation data for the most active station.


Hawaii Climate API
__________________________________________________

Overview

This project implements a Flask API for querying climate data from Hawaii. The data is stored in a SQLite database containing two tables: measurement and station. The API provides endpoints to retrieve precipitation, station information, and temperature observations for analysis.

Dependencies

Flask

SQLAlchemy

NumPy

Datetime

Database Setup

The SQLite database hawaii. sqlite is used to store climate data. SQLAlchemy is used to reflect the database tables and create a session for querying the data.

Flask Routes
1. Home Page

Route: /

Description: Displays a list of available API routes.

2. Precipitation Page
   
Route: /api/v1.0/precipitation

Description: Returns 12 months of precipitation data in JSON format.

4. Stations Page

Route: /api/v1.0/stations

Description: Returns a list of stations and their details in JSON format.

5. Temperature Observations (TOBs) Page

Route: /api/v1.0/tobs

Description: Returns temperature observations for the most active station in JSON format.

6. Dynamic Page - Start Date Only

Route: /api/v1.0/<start>

Description: Returns minimum, maximum, and average temperature data from the given start date in JSON format.

7. Dynamic Page - Start and End Date

Route: /api/v1.0/<start>/<end>

Description: Returns minimum, maximum, and average temperature data between the given start and end dates in JSON format.








