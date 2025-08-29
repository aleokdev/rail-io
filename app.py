from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

# API configuration
IRAIL_API_BASE = "https://api.irail.be"
MECHELEN_STATION = "Mechelen"
USER_AGENT = "MechelenTrainKiosk/1.0 (github.com/user/rail-io; contact@example.com)"

def get_train_departures():
    """Fetch train departures from Mechelen station"""
    try:
        url = f"{IRAIL_API_BASE}/liveboard/"
        params = {
            'station': MECHELEN_STATION,
            'format': 'json',
            'lang': 'en',
            'arrdep': 'departure'
        }
        
        headers = {
            'User-Agent': USER_AGENT
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract and format departure information
        departures = []
        if 'departures' in data and 'departure' in data['departures']:
            for departure in data['departures']['departure']:
                try:
                    # Convert timestamp to readable time
                    departure_time = datetime.fromtimestamp(int(departure['time']), tz=pytz.timezone('Europe/Brussels'))
                    
                    # Calculate delay in minutes
                    delay_seconds = int(departure.get('delay', '0'))
                    delay_minutes = delay_seconds // 60
                    
                    # Get platform information
                    platform = departure.get('platform', 'TBD')
                    
                    # Get train name from vehicle info
                    if 'vehicleinfo' in departure and 'shortname' in departure['vehicleinfo']:
                        train_name = departure['vehicleinfo']['shortname']
                    else:
                        train_name = departure.get('vehicle', 'Unknown')
                    
                    # Get destination from station field or stationinfo
                    destination = "Unknown"
                    if 'stationinfo' in departure and 'name' in departure['stationinfo']:
                        destination = departure['stationinfo']['name']
                    elif 'station' in departure:
                        destination = departure['station']
                    
                    departures.append({
                        'time': departure_time.strftime('%H:%M'),
                        'train': train_name,
                        'destination': destination,
                        'platform': platform,
                        'delay': delay_minutes,
                        'canceled': int(departure.get('canceled', '0')) == 1
                    })
                except (ValueError, KeyError, TypeError) as e:
                    print(f"Error processing individual departure: {e}")
                    print(f"Departure data: {departure}")
                    continue
        
        # Sort by departure time and limit to next 10 trains
        departures.sort(key=lambda x: x['time'])
        return departures[:10]
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []
    except Exception as e:
        print(f"Error processing data: {e}")
        return []

@app.route('/')
def index():
    """Main page showing train departures"""
    departures = get_train_departures()
    current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime('%H:%M')
    current_date = datetime.now(pytz.timezone('Europe/Brussels')).strftime('%A, %B %d, %Y')
    
    return render_template('index.html', 
                         departures=departures, 
                         current_time=current_time,
                         current_date=current_date,
                         station_name="Mechelen")

@app.route('/api/departures')
def api_departures():
    """API endpoint for getting departures data"""
    departures = get_train_departures()
    return jsonify(departures)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
