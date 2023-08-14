import os
from flask import Flask, send_from_directory, render_template, redirect
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

db_url = "postgres://fl0user:IxLtJgaZd1U4@ep-misty-cherry-32820023.ap-southeast-1.aws.neon.tech:5432/postgresbd?sslmode=require"

def get_db_params_from_url(url):
    result = urlparse(url)
    db_params = {
        'dbname': result.path.lstrip('/'),
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': result.port
    }
    return db_params

port = int(os.environ.get("PORT", 5000))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    try:
        db_params = get_db_params_from_url(db_url)
        connection = psycopg2.connect(**db_params)
        return "Conexión exitosa a la base de datos PostgreSQL"
    except (Exception, psycopg2.Error) as error:
        return "Error al conectar a la base de datos: " + str(error)



@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)
