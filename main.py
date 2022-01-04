from flask import Flask, json
from flask import render_template
import requests

app = Flask(__name__)


@app.route('/')
def standings():
    SECRET_KEY = ""
    id_competitions = '2021'
    api = 'https://api.football-data.org'
    uri = '/v2/competitions/' + id_competitions + '/standings'
    headers = { 'X-Auth-Token': SECRET_KEY }

    response = requests.get(api + uri, headers = headers)
    response.raise_for_status()
    content = response.json()
    table = content['standings'][0]['table']
    return render_template("index.html", data = table)
