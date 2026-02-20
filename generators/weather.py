"""Weather calendar generator."""

import requests
from datetime import datetime, timedelta
from utils import BaseCalendarGenerator
from config import CITIES, WEATHER_API_URL
from config.settings import WEATHER_CODE_MAP, WEATHER_FORECAST_DAYS


class WeatherGenerator(BaseCalendarGenerator):
    """Generate weather forecast calendars for cities."""
    
    def __init__(self, city='Ningbo', days=WEATHER_FORECAST_DAYS):
        """
        Initialize weather calendar generator.
        
        Args:
            city: City name (from CITIES config)
            days: Number of forecast days
        """
        self.city_info = CITIES.get(city, CITIES['Ningbo'])
        self.city_name = self.city_info['name']
        self.days = days
        
        super().__init__(f'{self.city_name}天气日历')
    
    def fetch_weather_data(self):
        """Fetch weather data from API."""
        url = (
            f"{WEATHER_API_URL}"
            f"?latitude={self.city_info['lat']}"
            f"&longitude={self.city_info['lon']}"
            f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
            f"&timezone=Asia/Shanghai"
            f"&forecast_days={self.days}"
        )
        
        response = requests.get(url)
        data = response.json()
        
        if 'daily' not in data:
            raise ValueError(f"Daily data not found in API response for {self.city_name}")
        
        return data['daily']
    
    def generate(self):
        """Generate weather calendar."""
        try:
            daily_data = self.fetch_weather_data()
            
            for i in range(self.days):
                date = datetime.now() + timedelta(days=i)
                temp_max = daily_data['temperature_2m_max'][i]
                temp_min = daily_data['temperature_2m_min'][i]
                weather_code = daily_data['weathercode'][i]
                
                weather_desc = WEATHER_CODE_MAP.get(weather_code, '☁️ 未知')
                summary = f"{self.city_name} {weather_desc} {int(temp_min)}°C ~ {int(temp_max)}°C"
                description = f"最高温度: {temp_max}°C\n最低温度: {temp_min}°C\n天气: {weather_desc}"
                
                self.add_event(
                    summary=summary,
                    start_date=date.date(),
                    description=description
                )
            
            return True
        except Exception as e:
            print(f"❌ Error generating weather for {self.city_name}: {e}")
            return False
    
    def generate_and_save(self, city_key):
        """
        Generate and save weather calendar for a city.
        
        Args:
            city_key: City key from CITIES config
        """
        self.__init__(city_key)
        if self.generate():
            self.save(f'weather_{city_key}.ics')
