"""
https://jinja.palletsprojects.com/en/latest/
https://flask.palletsprojects.com/en/3.0.x/
"""
from flask import Flask, render_template

app = Flask(__name__)


winners = [
    {'name': 'Albert Einstein', 'category': 'Physics'},
    {'name': 'V.S. Naipaul', 'category': 'Literature'},
    {'name': 'Dorothy Hodgkin', 'category': 'Chemistry'},
]


@app.route("/")  # the root route i.e., http://localhost:8000
def hello():
    return "Hello World!"


@app.route('/winners')
def winners_list():
    return render_template(
        'jinja_template.html',
        heading="A little winners' list",
        winners=winners
    )


if __name__ == "__main__":
    app.run(
        port=8000,  # localhost port the server will run on
        debug=True,  # useful logging to screen and in the event of an error, a browser-based report
    )

"""
Run:
python server_jinja.py

Open:
http://localhost:8000/winners

You see:
A little winners' list

    Albert Einstein , category: Physics
    V.S. Naipaul , category: Literature
    Dorothy Hodgkin , category: Chemistry
"""
