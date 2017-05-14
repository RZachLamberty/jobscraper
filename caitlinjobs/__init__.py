from flask import Flask, json, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

db = SQLAlchemy(app)

Bootstrap(app)


from .model import JobPosting
#from .forms import CommunityAttributesForm


@app.route('/')
def index():
    """present a table of job postings"""
    jobpostings = [j.to_json() for j in JobPosting.query.all()]
    return render_template("index.html", jobpostings=json.dumps(jobpostings))


app.debug = True

if __name__ == "__main__":
    app.run()
