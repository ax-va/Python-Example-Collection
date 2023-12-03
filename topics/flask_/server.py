from flask import Flask


app = Flask(__name__)


@app.route("/")  # the root route i.e., http://localhost:8000
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(
        port=8000,  # localhost port the server will run on
        debug=True,  # useful logging to screen and in the event of an error, a browser-based report
    )
"""
Run:

python server.py

 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 516-203-432

Open:
http://localhost:8000/

You see:
Hello World!
"""



