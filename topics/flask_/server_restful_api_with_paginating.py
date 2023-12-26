"""
This Flask example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/;
- https://flask-marshmallow.readthedocs.io/en/latest/;
- https://marshmallow-sqlalchemy.readthedocs.io/en/latest/.
"""
import os

import urllib.parse
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
CORS(app)  # Allow requests from any domain to access the data server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('../sqlite-databases/nobel_winners.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Winner(db.Model):
    """
    Object-relational mapping (ORM):
    This class will correspond to the table, the instances
    of this class will correspond to the rows of the table,
    and the class attributes correspond to the columns of the table.
    """
    __tablename__ = 'winners_cleaned'
    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    link = db.Column(db.String)
    year = db.Column(db.Integer)
    category = db.Column(db.String)
    country = db.Column(db.String)
    text = db.Column(db.Text)
    wikidata_code = db.Column(db.String)
    date_of_birth = db.Column(db.String)  # string form dates
    date_of_death = db.Column(db.String)  # string form dates
    place_of_birth = db.Column(db.String)
    place_of_death = db.Column(db.String)
    gender = db.Column(db.String)
    born_in = db.Column(db.String)
    award_age = db.Column(db.Integer)

    def __repr__(self):
        return f"<Winner(name='{self.name}', category='{self.category}', year={self.year})>"


class WinnerSchema(ma.Schema):
    """
    Serializing from the SQLite database into JSON-compliant data
    """
    class Meta:
        model = Winner
        fields = ('name', 'link', 'year', 'category', 'gender', 'country', 'born_in', 'award_age')


winner_schema = WinnerSchema()  # one record
winners_schema = WinnerSchema(many=True)  # multiple records


def make_pagination(url: str, results: dict):
    pagination = results['pagination']
    # Format a filter dict into a URL query
    query_str: str = urllib.parse.urlencode(results['filters'])

    page: int = pagination['page']
    per_page: int = pagination['per_page']
    num_pages: int = pagination["num_pages"]
    if page > 1:
        prev_page = url + f'?page={page-1}&per_page={per_page}&{query_str}'
    else:
        prev_page = ''

    if page < num_pages:
        next_page = url + f'?page={page+1}&per_page={per_page}&{query_str}'
    else:
        next_page = ''

    pagination['prev_page'] = prev_page
    pagination['next_page'] = next_page


class WinnersView(MethodView):
    def get(self):
        fields = ('year', 'category', 'gender', 'country', 'name', 'born_in', 'award_age')
        filters = request.args.to_dict()
        kwargs = {key: value for key, value in filters.items() if key in fields}
        app.logger.info(f"Filtering with the fields: {kwargs}")

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        winners = Winner.query.filter_by(**kwargs).paginate(page=page, per_page=per_page)
        winners_dumped = winners_schema.dump(winners.items)

        results = {
            "winners": winners_dumped,
            "filters": kwargs,
            "pagination":
                {
                    "count": winners.total,
                    "page": page,
                    "per_page": per_page,
                    "num_pages": winners.pages,
                },
        }

        make_pagination('winners/', results)
        return jsonify(results)

    def post(self):
        fields = winner_schema.fields
        kwargs = {key: value for key, value in request.json.items() if key in fields}
        app.logger.info(f"Creating a winner with the fields: {kwargs}")
        new_winner = Winner(**kwargs)
        db.session.add(new_winner)
        db.session.commit()
        result = winner_schema.jsonify(new_winner)
        return result


app.add_url_rule("/winners/", view_func=WinnersView.as_view("winners_view"))


class WinnerView(MethodView):
    def get(self, winner_id: str):
        winner = Winner.query.get_or_404(winner_id)
        result = winner_schema.jsonify(winner)
        return result

    def patch(self, winner_id):
        winner_to_update = Winner.query.get_or_404(winner_id)
        fields = winner_schema.fields
        kwargs = {key: value for key, value in request.json.items() if key in fields}
        app.logger.info(f"Updating the winner with the fields: {kwargs}")
        for key, value in kwargs.items():
            setattr(winner_to_update, key, value)
        db.session.commit()
        result = winner_schema.jsonify(winner_to_update)
        return result

    def delete(self, winner_id):
        winner_to_delete = Winner.query.get_or_404(winner_id)
        app.logger.info(f"Deleting the winner with id={winner_id}")
        db.session.delete(winner_to_delete)
        db.session.commit()
        return '', 204


app.add_url_rule("/winners/<winner_id>/", view_func=WinnerView.as_view("winner_view"))

if __name__ == "__main__":
    app.run(
        port=8000,  # localhost port the server will run on
        debug=True,  # useful logging to screen and in the event of an error, a browser-based report
    )

"""
$ curl -d category=Physics --get http://localhost:8000/winners/

{
  "filters": {
    "category": "Physics"
  },
  "pagination": {
    "count": 228,
    "next_page": "winners/?page=2&per_page=20&category=Physics",
    "num_pages": 12,
    "page": 1,
    "per_page": 20,
    "prev_page": ""
  },
  "winners": [
    {
      "award_age": 45,
      "born_in": null,
      "category": "Physics",
      "country": "Austria",
      "gender": "male",
      "link": "https://en.wikipedia.org/wiki/Wolfgang_Pauli",
      "name": "Wolfgang Pauli",
      "year": 1945
    },
    ...
    {
      "award_age": 40,
      "born_in": null,
      "category": "Physics",
      "country": "United States",
      "gender": "male",
      "link": "https://en.wikipedia.org/wiki/E._M._Purcell",
      "name": "E. M. Purcell",
      "year": 1952
    }
  ]
}

Get the next page:
$ curl -d category=Physics --get http://localhost:8000/winners/?page=2

Or open in the browser:
http://localhost:8000/winners/?category=Physics
http://localhost:8000/winners/?category=Physics&page=2
"""