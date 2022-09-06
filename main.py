from flask import Flask, json
from flask import render_template, jsonify
import requests
import datetime

app = Flask(__name__)

SECRET_KEY = str(os.getenv("API_KEY"))
id_competitions = '2021'
api = 'https://api.football-data.org'

fecha = datetime.datetime.utcnow()

def competition():
    competitionsUrl = '/v2/competitions/' + id_competitions
    headers = { 'X-Auth-Token': SECRET_KEY }
    response = requests.get(api + competitionsUrl, headers = headers)
    response.raise_for_status()
    content = response.json()
    currentSeason = content['currentSeason']
    matchday = currentSeason['currentMatchday']
    return str(matchday)

#Traer desde la API los datos para armar la tabla de posiciones
def standings():
    urlStandings = '/v2/competitions/' + id_competitions + '/standings'
    headers = { 'X-Auth-Token': SECRET_KEY }

    response = requests.get(api + urlStandings, headers = headers)
    response.raise_for_status()
    content = response.json()
    table = content['standings'][0]['table']
    return table

#Traer desde la API los datos para los resultados de los partidos
def matches():
    matchday = competition()
    urlMatches = '/v2/competitions/' + id_competitions + '/matches?matchday=' + matchday
    headers = { 'X-Auth-Token': SECRET_KEY }
    response = requests.get(api + urlMatches, headers = headers)
    response.raise_for_status()
    content = response.json()
    fixture = content['matches']
    return fixture


#Testear json
@app.route('/data_json')
def data_json():
    dummy_data = standings()
    return jsonify(dummy_data)

#Routeo a paginas.
@app.route('/')
@app.route('/home')
def home_page():
    partidos = matches()
    return render_template("index.html", data = partidos)

@app.route('/posiciones')
def tabla_page():
    posiciones = standings()
    return render_template("tabla.html", data = posiciones)

#Filtro para modificar el formato de las fechas
@app.template_filter('formatdatetime')
def format_datetime(value):
    cr_date = value
    new_date = datetime.datetime.strptime(cr_date[:10], '%Y-%m-%d')
    return new_date.strftime("%d-%m-%Y")
