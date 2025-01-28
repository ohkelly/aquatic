# Aquaponics AI Assistant

Welcome to the Aquaponics AI Assistant project AquaECO AI developed during AI for Energy Solution MIT 2025! This Streamlit app helps visualize real-time system performance metrics, including energy usage and water quality parameters, while also providing an AI assistant to assist with queries related to your aquaponics system.

## Features

- **Dashboard**: Displays real-time energy and water quality data.
  - View energy usage metrics from different sources like solar, biogas, and wind.
  - Analyze water quality parameters such as temperature and humidity.
- **AI Assistant**: Provides an interactive assistant for answering questions related to your aquaponics system, specifically energy usage and climate control, including CO2 emissions.

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/ohkelly/aquatic.git

##2. Navigate to the project directory:

cd aquatic
##3. Set up the virtual environment (optional but recommended):

python -m venv .venv
##4. Activate the virtual environment:
On Windows:

.venv\Scripts\activate
On macOS/Linux:

source .venv/bin/activate
5. Install dependencies:

pip install -r requirements.txt
6. Run the Streamlit app:

streamlit run app.py
The app will open in your default web browser.

##Project Structure
stackai_streamlit.py: The main Streamlit app file, where the layout and functionality are defined.
requirements.txt: A file containing the list of Python dependencies for the project.
data/: Folder containing the sample datasets for energy and water quality.
energy_data.csv: A CSV file with energy data (solar, biogas, wind).
sensor_data.csv: A CSV file with water quality data (temperature, humidity).
Features in Detail
Dashboard
The Dashboard allows you to monitor the performance of the aquaponics system in real-time. It loads data from CSV files containing energy usage and water quality parameters, and displays them in the following formats:

Energy Usage: A line chart showing energy usage from various sources (solar, biogas, wind).
Water Quality: An area chart showing temperature and humidity levels in the system.
AI Assistant
The AI Assistant provides an interactive assistant embedded within the app via an iframe. The assistant is designed to answer questions related to energy and climate control of your aquaponics system, including topics like CO2 emissions and system performance.

##Dependencies
The project requires the following Python packages:

streamlit: For building the app.
requests: To make HTTP requests (if necessary).
pandas: For data manipulation and reading CSV files.
plotly: For creating interactive charts and visualizations.
streamlit.components.v1: For embedding HTML components such as iframes.
logging: For logging and error tracking.
To install all dependencies, run:


pip install -r requirements.txt
##Troubleshooting
CSV File Loading Issues
If there are issues with loading the CSV files, ensure you have a stable internet connection as the app fetches the CSV files from raw GitHub links. If the data fails to load, try accessing the files directly from GitHub to ensure they are available.

##Missing Dependencies
If you run into issues with missing dependencies, make sure you have activated the virtual environment and installed the required packages:


pip install -r requirements.txt
##License
This project is licensed under the MIT License - see the LICENSE file for details.

##Acknowledgements
Streamlit: A powerful framework for building interactive web apps with Python.
Plotly: A great library for creating interactive charts and visualizations.
AI Assistant: The assistant integration is powered by Stack AI.
