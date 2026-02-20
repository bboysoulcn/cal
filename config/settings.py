"""Global settings for calendar service."""

import os

# Output directory for ICS files
OUTPUT_DIR = 'static/ics'

# Timezone
TIMEZONE = 'Asia/Shanghai'

# Weather API
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast'
WEATHER_FORECAST_DAYS = 7

# Weather code to description mapping
WEATHER_CODE_MAP = {
    0: '☀️ 晴天', 1: '🌤️ 晴朗', 2: '⛅ 多云', 3: '☁️ 阴天',
    45: '🌫️ 雾', 48: '🌫️ 雾凇',
    51: '🌦️ 小雨', 53: '🌧️ 中雨', 55: '🌧️ 大雨',
    61: '🌧️ 小雨', 63: '🌧️ 中雨', 65: '⛈️ 大雨',
    71: '🌨️ 小雪', 73: '🌨️ 中雪', 75: '❄️ 大雪',
    80: '🌦️ 阵雨', 81: '⛈️ 强阵雨', 82: '⛈️ 暴雨',
    95: '⛈️ 雷暴', 96: '⛈️ 冰雹', 99: '⛈️ 强雷暴'
}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
