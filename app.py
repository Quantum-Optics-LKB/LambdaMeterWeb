import json
import random, math, time
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)



# Triangular wave function for wavelength[0]
def triangular_wave(t, amplitude=0.5, period=10):
    return amplitude * (2 / math.pi) * math.asin(math.sin(2 * math.pi * t / period))


# Simulate WavelengthMeter data (replace with actual logic from your WavelengthMeter class)
def get_wavemeter_data():
    base_wavelengths = [460.861, 689.264, 679.289, 707.202, 921.724, 800.0, 650.0, 500.0]
    base_frequencies = [384229.18, 384227.29, 384232.37, 384229.26, 384230.5, 384231.0, 384228.5, 384227.0]

    # Introduce noise to the base data
    wavelengths_with_noise = [base + random.uniform(-0.01, 0.01) for base in base_wavelengths]
    frequencies_with_noise = [base + random.uniform(-0.5, 0.5) for base in base_frequencies]

       # Time-dependent triangular scan on wavelength[0]
    current_time = time.time()  # Get the current time in seconds
    amplitude = 0.1  # Define the amplitude of the triangular wave (in nm)
    period = 20  # Period of the triangular wave (in seconds)

    # Apply the triangular wave to wavelength[0]
    wavelengths_with_noise[0] = base_wavelengths[0] + triangular_wave(current_time, amplitude, period)


    return {
        "wavelengths": wavelengths_with_noise,
        "frequencies": frequencies_with_noise
    }

# Load the config.json file once when the app starts
with open('config.json') as config_file:
    config = json.load(config_file)

# Load the config.json file once when the app starts
def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)



# Serve the index.html page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/wave')
def wave():
    data = get_wavemeter_data()
    return render_template('index.html', channels=config["channels"], wavelengths=data['wavelengths'], precision=config["precision_wave"])

@app.route('/freq')
def freq():
    data = get_wavemeter_data()
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
    wavemeter_data = get_wavemeter_data()

    detunings = []
    for i, channel in enumerate(config["channels"]):
        reference_frequency = channel["reference_frequency"]
        detuning = wavemeter_data["frequencies"][i] - reference_frequency
        detunings.append(detuning)
    wavemeter_data["detunings"] = detunings

    emit('update_channels',  wavemeter_data)


if __name__ == '__main__':
    socketio.run(app, port=config["port"], debug=True)


    for i, channel in enumerate(config["channels"]):
        reference_frequency = channel["reference_frequency"]
        detuning = data["frequencies"][i] - reference_frequency
        detuning_values.append(detuning)