from flask import Flask, request, jsonify, render_template
import requests
import socket

app = Flask(__name__)

GREENCHECK_URL = "https://api.thegreenwebfoundation.org/api/v3/greencheck/"
IP2CO2_URL = "https://api.thegreenwebfoundation.org/api/v3/ip-to-co2intensity/"

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    hostname = data.get('hostname')

    if not hostname:
        return jsonify({"error": "Hostname is required"}), 400

    ip_address = get_ip_from_hostname(hostname)
    if not ip_address:
        return jsonify({"error": "Invalid hostname"}), 400

    greencheck_response = requests.get(f"{GREENCHECK_URL}{hostname}").json()
    ip2co2_response = requests.get(f"{IP2CO2_URL}{ip_address}").json()

    return jsonify({
        "greencheck": greencheck_response,
        "ip2co2": ip2co2_response
    })

if __name__ == '__main__':
    app.run(debug=True)
