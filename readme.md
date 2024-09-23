# Rubidium Wavemeter Interface

This project provides an interface for interacting with a High Finesse Wavemeter, displaying real-time wavelengths, frequencies, and detuning values. It includes a simple API and a front-end for viewing and updating the configuration. The application is built with Python, Flask, and JavaScript, and it uses WebSockets for real-time updates.

---

## Features

- ⚡ **Real-time display** of wavelengths, frequencies, and detuning values.
- 📊 **Channel-based detuning** calculation relative to reference frequencies.
- 🛠️ **Configurable channel names**, background colors, and reference frequencies.
- ✏️ **Editable configuration** through a web interface.
- 🔄 **Dynamic reloading** of the configuration without restarting the server.
- 📊 Live plotting of wavelengths, frequencies, and detuning values.

---


## Project Structure

- **`app.py`**: The main Flask server, responsible for routing and serving API endpoints.
- **`config.json`**: The configuration file where channels, reference frequencies, and other parameters are defined.
- **Templates**:
  - **`index.html`**: Displays the real-time wavelengths, frequencies, or detuning values for each channel.
  - **`detuning.html`**: (Optional) A page for viewing detuning values with respect to reference frequencies.
  - **`home.html`**: The homepage of the interface, providing navigation and links to the main functionality.
  - **`edit_config.html`**: A page for editing the configuration (channel labels, colors, etc.).
  - **`graph_wave.html, graph_freq.html, graph_detuning.html`**: Live plots for wavelengths, frequencies, and detuning.
- **Static Files**:
  - **CSS** and **JS** files for styling and dynamic behavior.

## Requirements

- Python 3.x
- Flask
- jQuery, D3.js, and Socket.io for the front-end
- Chart.js (for frontend charting)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install the dependencies**:
   Create and activate a Python virtual environment (if needed), then install the required packages.
   ```bash
   python -m venv venv
   source venv/bin/activate 
   pip install -r requirements.txt 
   # On Windows: 
   venv\Scripts\activate
   pip install -r .\requirements.txt
   ```

3. **Run the Flask app**:
   ```bash
   pyhton app.py
   ```

4. **Access the application**:
   Open a browser and navigate to `http://localhost:8000` (or the port specified in `config.json`).

## Configuration

The configuration is stored in `config.json` and is structured as follows:

```json
{
  "precision_wave": 6,
  "precision_freq": 3,
  "port": 8000,
  "channels": [
    { "i": 0, "label": "Shakdag - 1D", "background": "#300", "reference_frequency": 384229.18 },
    { "i": 1, "label": "Aoraki - Hydro", "background": "#030", "reference_frequency": 384227.29 },
    { "i": 2, "label": "Kosciusko - Fluide Hydro", "reference_frequency": 384232.37 },
    ...
  ]
}
```
- **precision_wave**: Number of digits for wavelengths.
- **precision_freq**: Number of digits for frequencies.
- **port**: The port on which the server runs.
- **channels**: An array of channel configurations, each with a label, background color, and reference frequency.
- **background**: The background color for the channel display.

## Main API Endpoints

- **GET /api/wavelengths**: Returns all wavelengths.
- **GET /api/frequencies**: Returns all frequencies.
- **GET /api/detuning**: Returns detuning values relative to the reference frequencies.
- **POST /api/reload_config**: Reloads the `config.json` file without restarting the server.
- **POST /api/config**: Updates the configuration.

## Web Interface

- **Home Page**: Provides navigation to view wavelengths, frequencies, and detuning.
- **Wave/Freq Pages**: Displays real-time data for each channel.
- **Detuning Page**: Shows detuning relative to each channel’s reference frequency.
- **Edit Config Page**: Allows updating channel names, background colors, and reference frequencies.

## Live Graphs for Wavelength, Frequency, and Detuning

- Access the live wavelength graph for a specific channel:
  ```
  http://localhost:5000/graph/wave/<channel_id>
  ```

- Access the live frequency graph for a specific channel:
  ```
  http://localhost:5000/graph/freq/<channel_id>
  ```

- Access the live detuning graph for a specific channel:
  ```
  http://localhost:5000/graph/detuning/<channel_id>
  ```

## How to Edit Configuration

1. Navigate to `/edit_config` to update the current configuration (channel names, colors, etc.).
2. Save the configuration, and the app will reload with the updated settings.

## How to Reload Configuration

If you manually update `config.json`, you can reload it without restarting the server:

1. Click the "Reload Config" button on the homepage, or
2. Send a `POST` request to `/api/reload_config`.

## Configure your local hostname
If you want to access it without remembering the IP, you can configure your local hostname to point to the server.
### Windows
1. Open the file `C:\Windows\System32\drivers\etc\hosts` in a text editor.
2. Add the following line at the end of the file:
   ``` 10.0.2.3 wlm.local ```
3. Save the file and access the application at `http://wlm.local:5000`.
### MacOS/Linux
1. Open the file `/etc/hosts` in a text editor.
2. Add the following line at the end of the file:
   ``` 10.0.2.3 wlm.local ```
3. Save the file and access the application at `http://wlm.local:5000`.

## License

This project is open-source. Feel free to modify and use it for your own purposes.

---

