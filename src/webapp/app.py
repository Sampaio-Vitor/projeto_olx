from flask import Flask, render_template
import pandas as pd
from datetime import datetime
import boto3
import io
from io import StringIO

s3 = boto3.client('s3',
                  aws_access_key_id='AKIARZZDJ5FLJQOG2IN7',
                  aws_secret_access_key='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',
                  region_name='sa-east-1')
bucket_name = 'bucketolx'

app = Flask(__name__)

@app.route('/')
def index():
    # Load the data from the CSV file
    df = read_from_s3("data/scored_data.csv")

    # Convert DATE_SCRAPE to datetime format
    df['DATE_SCRAPE'] = pd.to_datetime(df['DATE_SCRAPE'])
        
    # Get today's and yesterday's date
    today = pd.Timestamp.now().normalize()
    yesterday = today - pd.Timedelta(days=1)

    # Filter the DataFrame to only include rows where DATE_SCRAPE is today or yesterday
    df = df[df['DATE_SCRAPE'].dt.normalize().isin([today, yesterday])]
    
    # Filter the DataFrame to only include rows where DATE_SCRAPE is today
    df = df[df['DATE_SCRAPE'].dt.normalize() == today]
    
    # Extract the desired columns
    df = df[["TITLE", "LINK", "DATE_SCRAPE", "NEIGHBORHOOD", "CONDO", "TAX", "AREA", "ROOMS_NO", "BATH_NO", "PARKING_SPOTS", "PRICE", "Predictions"]]
    
    # Calculate the percentage difference
    df["Difference%"] = ((df["Predictions"] - df["PRICE"]) / df["PRICE"]) * 100

    # Calculate the number of 🔥 symbols
    df["Hotness"] = df["Difference%"].apply(lambda x: '🔥' * (1 if x > 10 else 0) + '🔥' * (1 if x > 20 else 0) + '🔥' * (1 if x > 30 else 0))
    
    # Add "Região" column from NEIGHBORHOOD
    df["Bairro"] = df["NEIGHBORHOOD"]

    # Sort by difference
    df = df[df["Difference%"] > 0].sort_values(by="Difference%", ascending=False)

    # Extracting the date from DATE_SCRAPE for the first record (as they should all be the same in this context)
    if len(df) > 0:
        date_str = df.iloc[0]["DATE_SCRAPE"]
        date_obj = date_str.to_pydatetime()  # As DATE_SCRAPE is already in datetime format
        formatted_date = date_obj.strftime('%d/%m/%Y')
    else:
        formatted_date = today.strftime('%d/%m/%Y')

    # Convert dataframe to a list of dictionaries to make it easier to iterate over in the template
    records = df.to_dict(orient="records")
    
    return render_template('index.html', records=records, today_date=formatted_date)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
