# SQLAlchemy Challenge

## Part 1 Analyze and Explore the Climate Data
Using Python and SQLAlchemy I did a basic climate analysis and data exploration of the climate database. More specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib.
- Precipitation Analysis:
  - Found the most recent date in the dataset
  - With that date, I found the previous 12 months of precipitation data by querying the previous 12 months of data
  - I selected only the "date" and "prcp" values
  - Loaded the query results into a Pandas DataFrame. Explicitly set the column names.
  - I sorted the DataFrame values by "date".
  - Plotted the results by using the DataFrame plot method and using Pandas I printed the summary statistics for the precipitation data
 
- Station Analysis:
  - I designed a query to calculate the total number of stations in the dataset
  - I designed a query to find the most-active stations
  - I designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
  - I designed a query to get the previous 12 months of temperature observation (TOBS) data.
  - I also queryed the previous 12 months of TOBS data for that station and plotted the results as a histogram

## Part 2 Design Your Climate App
I designed a Flask API based on the queries that I developed.
- I created a homepage and the following available routes:
  - /api/v1.0/precipitation
  - /api/v1.0/stations
  - /api/v1.0/tobs
  - /api/v1.0/<start>
  /api/v1.0/<start>/<end>
