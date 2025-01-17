from flask import Flask, render_template, jsonify
import pandas as pd


# Initialize the Flask application
app = Flask(__name__)

# Read the CSV file containing station information
stations = pd.read_csv("data/stations.txt", skiprows=17)

# Strip extra spaces from column names
stations.columns = stations.columns.str.strip()

# Select only the 'STAID' and 'STANAME' columns
station = stations[["STAID", "STANAME"]]


# Define the home route to render the home page with station information
@app.route("/")
def home():
    return render_template("home.html", data=station.to_html())


# Define the route to get temperature data for a specific station and date
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # Construct the filename based on the station ID
    filename = ("data/TG_STAID" + str(station).zfill(6) + ".txt")
    
    # Read the data file and parse the dates
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    
    # Filter out invalid temperature values
    df = df[df['   TG'] != -9999]
    
    # Get the temperature for the specified date and convert to Celsius
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    
    # Return the temperature data as JSON
    return {"station": station,
            "date": date,
            "temperature": temperature}


# Define the route to get all data for a specific station
@app.route("/api/v1/<station>")
def all_data(station):
    # Construct the filename based on the station ID
    filename = ("data/TG_STAID" + str(station).zfill(6) + ".txt")
    
    # Read the data file and parse the dates
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    
    # Filter out invalid temperature values
    df = df[df['   TG'] != -9999]
    
    # Convert the data to a dictionary format
    result = df.to_dict(orient="records")
    
    # Return the data as JSON
    return jsonify(result)


# Define the route to get yearly data for a specific station and year
@app.route("/api/v1/yearly/<station>/<year>")
def yearly_data(station, year):
    # Construct the filename based on the station ID
    filename = ("data_small/TG_STAID" + str(station).zfill(6) + ".txt")

    # Read the data file
    df = pd.read_csv(filename, skiprows=20)

    # Convert the 'DATE' column to string
    df['    DATE'] = df['    DATE'].astype(str)

    # Filter the data for the specified year
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    
    # Return the filtered data as JSON
    return jsonify(result)


# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)