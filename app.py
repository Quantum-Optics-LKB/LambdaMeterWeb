import json
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from wlm import WavelengthMeter, get_wavemeter_data

app = Flask(__name__)
socketio = SocketIO(app)

# Instantiate WavelengthMeter (set debug=True for dummy data)
wlm = WavelengthMeter(debug=False)  


def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)
# Load the config.json file once when the app starts
load_config()

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/wave')
def wave():
    data = get_wavemeter_data(wlm)
    return render_template('index.html', channels=config["channels"], wavelengths=data['wavelengths'], precision=config["precision_wave"])

@app.route('/freq')
def freq():
    data = get_wavemeter_data(wlm)
    return render_template('index.html', channels=config["channels"], frequencies=data['frequencies'], precision=config["precision_freq"])

@app.route('/detuning')
def detuning():
    detuning_values = [1]
    return render_template('index.html',  channels=config["channels"], detunings=detuning_values,  precision=config["precision_freq"])

@app.route('/freq/graph/<int:channel_id>')
def graph_freq(channel_id):
    return render_template('graph_freq.html', channel_id=channel_id-1)

@app.route('/wave/graph/<int:channel_id>')
def graph_wave(channel_id):
    return render_template('graph_wave.html', channel_id=channel_id-1)

@app.route('/detuning/graph/<int:channel_id>')
def graph_detuning(channel_id):
    return render_template('graph_detuning.html', channel_id=channel_id-1)

# API routes
# API route to get all wavelengths
@app.route('/api/', methods=['GET'])
def get_data():
    data = get_wavemeter_data(wlm)
    return jsonify(data)

# API route to get all wavelengths
@app.route('/api/wave', methods=['GET'])
def get_wavelengths():
    data = get_wavemeter_data(wlm)
    return jsonify(data['wavelengths'])

# API route to get all frequencies
@app.route('/api/freq', methods=['GET'])
def get_frequencies():
    data = get_wavemeter_data(wlm)
    return jsonify(data['frequencies'])

# API route to get a specific channel's wavelength
@app.route('/api/wave/<int:channel>', methods=['GET'])
def get_wavelength_channel(channel):
    data = get_wavemeter_data(wlm)
    return jsonify(data['wavelengths'][channel])

# API route to get a specific channel's frequency
@app.route('/api/freq/<int:channel>', methods=['GET'])
def get_frequency_channel(channel):
    data = get_wavemeter_data(wlm)
    return jsonify(data['frequencies'][channel])

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
def update_config():
    new_config = request.json
    save_config(new_config)
    global config
    config = new_config  # Update the global config
    return jsonify({"message": "Config updated successfully!"})

@app.route('/config')
def edit_config():
    return render_template('edit_config.html')

@app.route('/api/reload_config', methods=['POST'])
def reload_config():
    global config
    # Reload the configuration from the file
    config = load_config()
    return jsonify({"message": "Config reloaded successfully!"}), 200

config = load_config()


# WebSocket handler for real-time updates
@socketio.on('request_update')
def handle_request_update():
    wavemeter_data = get_wavemeter_data(wlm)

    detunings = []
    for i, channel in enumerate(config["channels"]):
        reference_frequency = channel["reference_frequency"]
        detuning = wavemeter_data["frequencies"][i] - reference_frequency
        detunings.append(detuning)
    wavemeter_data["detunings"] = detunings

    emit('update_channels',  wavemeter_data)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=config["port"], debug=False)