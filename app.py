from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
from flask import redirect
from flask_session import Session
import os
import requests


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy(app)


class Users(db.Model):
    _id= db.Column("id", db.Integer, primary_key=True)
    state = db.column("state", db.VARCHAR)
    username = db.column("username", db.String(100))

    def __init__(self, username, state):
        self.username = username
        self.state = state

oauth = OAuth(app)

API_BASE = os.getenv('API_BASE')
ACCESS_TOKEN_URL = os.getenv('ACCESS_TOKEN_URL')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "patient/ExplanationOfBenefit.read patient/Coverage.read patient/Patient.read profile"
username= 'BBUser00000'
password= 'PW00000!'
client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)


@app.route('/')
def welcome():
    return "Welcome to EMR Integration with Bluebutton"

@app.route('/login/callback')
def bluebutton_login_callback():
    authorization_response = request.url;
    session["oauth_code"] = request.args.get('code')
    print(authorization_response);
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, state=session['oauth_state'])
    token = client.fetch_token(ACCESS_TOKEN_URL, authorization_response=authorization_response)
    session['oauth_token'] = token
    return redirect('/patient/profile')

@app.route('/auth/login')
def bluebutton_login():
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    uri, state = client.create_authorization_url(API_BASE)
    print(state)
    session["oauth_state"] = state
    return redirect(uri)

@app.route('/patient/profile')
def patient_profile():
    client_url = OAuth2Session(CLIENT_ID,CLIENT_SECRET, token=session['oauth_token'])
    profile_url ="https://sandbox.bluebutton.cms.gov/v2/fhir/Patient"
    return jsonify(client_url.get(profile_url).json());

@app.route('/patient/explanation_of_benefit')
def explanation_of_benefit():
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, token=session['oauth_token'])
    explanation_of_benefit_url ="https://sandbox.bluebutton.cms.gov/v2/fhir/Coverage"
    return jsonify(client.get(explanation_of_benefit_url).json());

@app.route('/patient/coverage')
def coverage():
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, token=session['oauth_token'])
    coverage_url ="https://sandbox.bluebutton.cms.gov/v2/fhir/Coverage"
    return jsonify(client.get(coverage_url).json());

@app.route('/patient/re-authorize')
def reauthorize():
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, state=session['oauth_state'])
    authorization_response ='http://127.0.0.1:5000/login/callback?code='+session['oauth_code']+'&state='+session['oauth_state']
    token = client.fetch_token(ACCESS_TOKEN_URL, method="GET", authorization_response=authorization_response)
    session['oauth_token'] = token
    return {};


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)