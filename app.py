from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the dataset into memory
data = pd.read_csv("NYC_Wi-Fi_Hotspot_Locations.csv")

@app.route("/")
def index():
    # Extract unique borough names for the dropdown list
    boroughs = data["Borough"].dropna().unique()
    boroughs = sorted([borough.upper() for borough in boroughs])  # Capitalize boroughs
    
    # Extract unique provider names for the dropdown list
    providers = data["Provider"].dropna().unique()
    providers = sorted([provider.title() for provider in providers])  # Capitalize providers

    return render_template("index.html", boroughs=boroughs, providers=providers)

@app.route("/search", methods=["GET"])
def search():
    borough = request.args.get("borough", "").upper()
    provider = request.args.get("provider", "").title()

    # Filter data
    filtered_data = data
    if borough:
        filtered_data = filtered_data[filtered_data["Borough"].str.upper() == borough]
    if provider:
        filtered_data = filtered_data[filtered_data["Provider"].str.title() == provider]

    # Replace NaN with null or empty string
    filtered_data = filtered_data.where(pd.notnull(filtered_data), None)

    # Return filtered data as JSON
    return jsonify(filtered_data.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
