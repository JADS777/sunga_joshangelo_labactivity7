## Overview
This program is a command-line Weather & Air Quality Visualizer developed in Python. It demonstrates external API data mining, data processing with pandas, and interactive data visualization with Plotly. By fetching live hourly forecast data for 16 cities in the National Capital Region (NCR) and merging it into a single dataset, it shows how two independent APIs can be combined into one interactive dashboard that a user can explore in a browser.

## Architecture
The system is built using interrelated components that separate the menu-driven controller from the data fetching/processing logic and the external data sources:
1. Main Loop (main): Serves as the controller for the whole program. It displays the menu of NCR cities, reads the user's numeric input in a while loop, and dispatches the selected city to fetch_and_visualize.
2. Data Fetching & Processing (fetch_and_visualize): Handles everything related to a single visualization request — calling both external APIs, converting the JSON responses into pandas DataFrames, merging the weather and air quality data on their shared time column, and trimming the result to a 72-hour window.
3. Visualization & Output: Builds a dual-line Plotly chart (temperature vs. PM2.5) from the merged DataFrame, writes it to dashboard.html, and attempts to open it automatically in the default browser (via WSL/Windows interop), falling back to a manual-open message if that fails.
4. External APIs (Open-Meteo Weather API, Open-Meteo Air Quality API): The live data sources, queried fresh on every request using the selected city's latitude and longitude, with no local database or persistent storage involved.

```
+-------------------------+
|        Main Loop        |
|          (main)         |
+-------------------------+
             |
             v
+-------------------------+
|   Data Fetching &       |
|   Processing             |
| (fetch_and_visualize)   |
+-------------------------+
      |              |
      v              v
+-------------+  +-------------+
|  Weather    |  | Air Quality |
|  API        |  |    API      |
| (Open-Meteo)|  | (Open-Meteo)|
+-------------+  +-------------+
      |              |
      +------+  +----+
             v  v
      +-------------------------+
      |   Merged DataFrame      |
      |  (time, temp, PM2.5)    |
      +-------------------------+
                  |
                  v
      +-------------------------+
      |   Plotly Dashboard      |
      |    (dashboard.html)     |
      +-------------------------+
```

## How to Run
1. Ensure Python3 is installed.
2. Install the required libraries: `pip install requests pandas plotly`.
3. Ensure `main.py` is run with an active internet connection, since it queries the Open-Meteo APIs live on every request.
4. Run the program: `python3 main.py`.
5. Use the on-screen menu to select a city by number. A dashboard.html file is generated for that city and, if running in WSL with Windows interop available, opens automatically in the default browser; otherwise, open dashboard.html manually from the project folder.
6. Enter 0 at any time to exit.
