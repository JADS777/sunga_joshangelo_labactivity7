import os
import subprocess
import webbrowser
import requests
import pandas as pd
import plotly.graph_objects as go

def fetch_and_visualize(city_name, lat, lon):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&timezone=auto"
    aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5&timezone=auto"
    
    try:
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        aqi_response = requests.get(aqi_url, timeout=10)
        aqi_response.raise_for_status()
        aqi_data = aqi_response.json()
        
        df_weather = pd.DataFrame({
            "time": pd.to_datetime(weather_data["hourly"]["time"]),
            "Temperature (°C)": weather_data["hourly"]["temperature_2m"]
        })
        
        df_aqi = pd.DataFrame({
            "time": pd.to_datetime(aqi_data["hourly"]["time"]),
            "PM2.5 (μg/m³)": aqi_data["hourly"]["pm2_5"],
        })
        
        df_merged = pd.merge(df_weather, df_aqi, on="time").dropna()
        df_plot = df_merged.head(72)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_plot["time"], 
            y=df_plot["Temperature (°C)"],
            mode='lines',
            name='Temperature (°C)',
            line=dict(color='red', dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=df_plot["time"], 
            y=df_plot["PM2.5 (μg/m³)"],
            mode='lines',
            name='PM2.5 Air Quality',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title=f"72-Hour Forecast: Temperature vs PM2.5 in {city_name}",
            xaxis_title="Date & Time",
            yaxis_title="Measurements",
            legend_title="Legend",
            hovermode="x unified"
        )
        
        output_file = "dashboard.html"
        fig.write_html(output_file)
        
        full_path = os.path.abspath(output_file)
        try:
            win_path = subprocess.check_output(["wslpath", "-w", full_path]).decode().strip()
            subprocess.run(["cmd.exe", "/c", "start", '""', win_path], shell=False)
            print(f"Graph opened successfully for {city_name}!\n")
        except Exception as e:
            print(f"Could not auto-open the browser: {e}")
            print(f"Dashboard saved to {full_path} — open it manually in your browser.\n")

    except requests.exceptions.RequestException as e:
        print(f"Network or API error occurred: {e}\n")
    except KeyError as e:
        print(f"Data parsing error. Missing expected data key: {e}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}\n")

def main():
    locations = {
        1: ("Caloocan", 14.6488, 120.9678),
        2: ("Las Piñas", 14.4445, 120.9939),
        3: ("Makati", 14.5547, 121.0244),
        4: ("Malabon", 14.6733, 120.9397),
        5: ("Mandaluyong", 14.5794, 121.0359),
        6: ("Manila (the capital city)", 14.5995, 120.9842),
        7: ("Marikina", 14.6481, 121.1133),
        8: ("Muntinlupa", 14.4081, 121.0415),
        9: ("Navotas", 14.6667, 120.9500),
        10: ("Parañaque", 14.4793, 121.0198),
        11: ("Pasay", 14.5378, 120.9993),
        12: ("Pasig", 14.5764, 121.0851),
        13: ("Quezon City", 14.6760, 121.0437),
        14: ("San Juan", 14.6019, 121.0355),
        15: ("Taguig", 14.5176, 121.0509),
        16: ("Valenzuela", 14.7011, 120.9830),
    }

    while True:
        print("----------------------------------------")
        print("  NCR Weather & Air Quality Visualizer  ")
        print("----------------------------------------")
        for num, (city, _, _) in locations.items():
            print(f"[{num}] {city}")
        print("[0] Exit")
        
        choice = input("\nEnter location number: ").strip()
        
        try:
            choice_int = int(choice)
            if choice_int == 0:
                print("Exiting program.")
                break
            elif choice_int in locations:
                city, lat, lon = locations[choice_int]
                print(f"\nFetching data for {city}...")
                fetch_and_visualize(city, lat, lon)
            else:
                print("Invalid number. Please select a valid option from the menu.\n")
        except ValueError:
            print("Invalid input. Please enter an integer number.\n")

if __name__ == "__main__":
    main()
