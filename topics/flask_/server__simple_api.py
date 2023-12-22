"""
This Flask example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023.
"""
import pandas as pd
from flask import Flask, request, abort


app = Flask(__name__)


@app.route('/api/winners')
def get_country_data():
    df = pd.read_parquet('../parquet-files/nobel_winners_cleaned.parquet')
    print(f"Request args: {dict(request.args)}")
    total_query = ""
    country = request.args.get("country")
    category = request.args.get("category")
    year = request.args.get("year")

    if country:
        total_query = f"country == '{country}'" if not total_query else total_query + f"and country == '{country}'"
    if category:
        total_query = f"category == '{category}'" if not total_query else total_query + f"and category == '{category}'"
    if year:
        total_query = f"year == {year}" if not total_query else total_query + f"and year == {year}"

    if total_query:
        df_result = df.query(total_query)
    else:
        abort(404)  # Resource not found

    if len(df_result) > 0:
        return df_result.to_json(orient="records")


if __name__ == '__main__':
    app.run(port=8000, debug=True)


"""
Run Flask:
$ python server__simple_api.py

Open:
http://localhost:8000/api/winners?country=Japan&catagory=Physics

Or use in the commnad line:
$ curl -d category=Physics -d country=Japan --get http://localhost:8000/api/winners
"""
