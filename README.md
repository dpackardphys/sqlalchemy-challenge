# sqlalchemy-challenge

For analysis of measurement and station datasets, see climate_midway.ipynb

To run the Flask API, run app.py and open the url (default: http://127.0.0.1:5000/) in a web browser.
Available routes:
/api/v1.0/precipitation
  - Return JSON dictionary of last 12 months of precipitation data.
/api/v1.0/stations
  - Return a JSON list of stations
/api/v1.0/tobs
  - Returns JSONified data of temperature observations from the previous year at most active station
/api/v1.0/<start>
  - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range (inclusive).
  - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
  - Date formate: YYYY-MM-DD
/api/v1.0/<start>/<end>
  - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start and end range (inclusive).
  - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start and end dates.
  - Date formate: YYYY-MM-DD
