import json
import random
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Simulate WavelengthMeter data (replace with actual logic from your WavelengthMeter class)
def get_wavemeter_data():
    base_wavelengths = [460.861, 689.264, 679.289, 707.202, 921.724, 800.0, 650.0, 500.0]
    base_frequencies = [384229.18, 384227.29, 384232.37, 384229.26, 384230.5, 384231.0, 384228.5, 384227.0]

    # Introduce noise to the base data
    wavelengths_with_noise = [base + random.uniform(-0.01, 0.01) for base in base_wavelengths]
    frequencies_with_noise = [base + random.uniform(-0.5, 0.5) for base in base_frequencies]

    return {
        "wavelengths": wavelengths_with_noise,
        "frequencies": frequencies_with_noise
    }

# Load the config.json file once when the app starts
with open('config.json') as config_file:
    config = json.load(config_file)


# Serve the index.html page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/wave')
def wave():
    data = get_wavemeter_data()
    return render_template('index.html', channels=config["channels"], wavelengths=data['wavelengths'], precision=config["precision"])

@app.route('/freq')
def freq():
    data = get_wavemeter_data()
    return render_template('index.html', channels=config["channels"], frequencies=data['frequencies'], precision=config["precision"])

# API route to get all wavelengths
@app.route('/api/', methods=['GET'])
def get_data():
    data = get_wavemeter_data()
    return jsonify(data)

# API route to get all wavelengths
@app.route('/api/wave', methods=['GET'])
def get_wavelengths():
    data = get_wavemeter_data()
    return jsonify(data['wavelengths'])

# API route to get all frequencies
@app.route('/api/freq', methods=['GET'])
def get_frequencies():
    data = get_wavemeter_data()
    return jsonify(data['frequencies'])

# API route to get a specific channel's wavelength
@app.route('/api/wave/<int:channel>', methods=['GET'])
def get_wavelength_channel(channel):
    data = get_wavemeter_data()
    return jsonify(data['wavelengths'][channel])

# API route to get a specific channel's frequency
@app.route('/api/freq/<int:channel>', methods=['GET'])
def get_frequency_channel(channel):
    data = get_wavemeter_data()
    return jsonify(data['frequencies'][channel])

# WebSocket handler for real-time updates
@socketio.on('request_update')
def handle_request_update():
    wavemeter_data = get_wavemeter_data()
    emit('update_channels', wavemeter_data)

    # channel = json.get('channel', 0)
    # data_type = json.get('type', 'wavelengths')
    # data = get_wavemeter_data()
    # value = data[data_type][channel]
    # emit('update_data', {'value': value, 'timestamp': time.time()})
    # wavemeter_data = get_wavemeter_data()
    # emit('update_channels', wavemeter_data)

if __name__ == '__main__':
    socketio.run(app, port=config["port"], debug=True)
