"""
This Flask example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/;
- https://flask-marshmallow.readthedocs.io/en/latest/;
- https://marshmallow-sqlalchemy.readthedocs.io/en/latest/.
"""
import os
from flask import Flask, request
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


class WinnersView(MethodView):
    def get(self):
        fields = ('year', 'category', 'gender', 'country', 'name', 'born_in', 'award_age')
        filters = request.args.to_dict()
        kwargs = {key: value for key, value in filters.items() if key in fields}
        app.logger.info(f"Filtering with the fields: {kwargs}")
        winners = Winner.query.filter_by(**kwargs)
        result = winners_schema.jsonify(winners)
        return result

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
Add a new winner:
$ curl http://localhost:8000/winners/ -X POST -H "Content-Type: application/json" -d '{"category":"Computer Science","year":2024,"name":"Alexander Vasiliev","country":"Germany"}'

{
  "award_age": null,
  "born_in": null,
  "category": "Computer Science",
  "country": "Germany",
  "gender": null,
  "link": null,
  "name": "Alexander Vasiliev",
  "year": 2024
}

Get a winner:
http://localhost:8000/winners/?name=Alexander%20Vasiliev

[
  {
    "award_age": null,
    "born_in": null,
    "category": "Computer Science",
    "country": "Germany",
    "gender": null,
    "link": null,
    "name": "Alexander Vasiliev",
    "year": 2024
  }
]

http://localhost:8000/winners/975/

{
  "award_age": null,
  "born_in": null,
  "category": "Computer Science",
  "country": "Germany",
  "gender": null,
  "link": null,
  "name": "Alexander Vasiliev",
  "year": 2024
}

Update a winner:
$ curl http://localhost:8000/winners/975/ -X PATCH -H "Content-Type: application/json" -d '{"award_age":"38"}'

{
  "award_age": 38,
  "born_in": null,
  "category": "Computer Science",
  "country": "Germany",
  "gender": null,
  "link": null,
  "name": "Alexander Vasiliev",
  "year": 2024
}

Delete a winner:
$ curl http://localhost:8000/winners/975/ -X DELETE -H "Content-Type: application/json"

http://localhost:8000/winners/975/

Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
"""