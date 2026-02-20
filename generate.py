import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import json
import os

# Create static/ics directory if not exists
os.makedirs('static/ics', exist_ok=True)

def generate_weather_calendar(city='Ningbo', days=7):
    # Use open-meteo API (free, no key)
    url = f"https://api.open-meteo.com/v1/forecast?latitude=29.8683&longitude=121.5440&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Shanghai&forecast_days={days}"
    response = requests.get(url)
    data = response.json()
    if 'daily' not in data:
        print("API response:", data)
        raise ValueError("Daily data not found in API response")
    
    cal = Calendar()
    cal.add('prodid', '-//Weather Calendar//')
    cal.add('version', '2.0')
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        temp_max = data['daily']['temperature_2m_max'][i]
        temp_min = data['daily']['temperature_2m_min'][i]
        weather_code = data['daily']['weathercode'][i]
        
        # Simple weather description
        weather_desc = {0: 'Sunny', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 61: 'Rain'}.get(weather_code, 'Unknown')
        
        event = Event()
        event.add('summary', f"Weather: {weather_desc}, {temp_min}°C - {temp_max}°C")
        event.add('dtstart', date.date())
        event.add('dtend', (date + timedelta(days=1)).date())
        cal.add_component(event)
    
    with open(f'static/ics/weather_{city}.ics', 'wb') as f:
        f.write(cal.to_ical())

def generate_holidays_calendar():
    # Hardcoded 2024 Chinese holidays (example)
    holidays = [
        {'date': '2024-01-01', 'name': 'New Year'},
        {'date': '2024-02-10', 'name': 'Spring Festival'},
        # Add more
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//Holidays Calendar//')
    cal.add('version', '2.0')
    
    for h in holidays:
        event = Event()
        event.add('summary', h['name'])
        event.add('dtstart', datetime.fromisoformat(h['date']).date())
        event.add('dtend', (datetime.fromisoformat(h['date']) + timedelta(days=1)).date())
        cal.add_component(event)
    
    with open('static/ics/holidays.ics', 'wb') as f:
        f.write(cal.to_ical())

# Add more functions for lunar, zodiac, countdown

if __name__ == '__main__':
    generate_weather_calendar()
    generate_holidays_calendar()
    print("ICS files generated.")