from flask import Flask, request, jsonify, session, url_for
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
from flask import redirect
from flask_session import Session
import os


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

oauth = OAuth(app)

API_BASE = os.getenv('API_BASE')
ACCESS_TOKEN_URL = os.getenv('ACCESS_TOKEN_URL')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "patient/ExplanationOfBenefit.read patient/Coverage.read patient/Patient.read profile"
username= 'BBUser00000'
password= 'PW00000!'

@app.route('/')
def welcome():
    return "Welcome to EMR Integration app";

@app.route('/login/callback')
def bluebutton_login_callback():
    authorization_response = request.url;
    print(session.get('oauth_state'))
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, state=session['oauth_state'])
    token = client.fetch_token(ACCESS_TOKEN_URL, authorization_response=authorization_response)
    session['oauth_token'] = token
    print(token)
    return redirect('/patient/profile')

@app.route('/auth/login')
def bluebutton_login():
    client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    uri, state = client.create_authorization_url(API_BASE)
    session["oauth_state"] = state
    return redirect(uri)

@app.route('/patient/profile')
def patient_profile():
    client = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    profile_url ="https://sandbox.bluebutton.cms.gov/v2/fhir/Patient?patient=-20140000010000"
    return jsonify(client.get(profile_url).json());

@app.route('/patient/explanation_of_benefit')
def explanation_of_benefit():
    client = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    explanation_of_benefit_url ="https://sandbox.bluebutton.cms.gov/v2/fhir/Coverage"
    return jsonify(client.get(explanation_of_benefit_url).json());

@app.route('/patient/coverage')
def coverage():
    client = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    coverage_url ="https://sandbox.bluebutton.cms.gov/v2/fhir/Coverage"
    return jsonify(client.get(coverage_url).json());


if __name__ == '__main__':
    app.run(debug=True)
