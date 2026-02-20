import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import json
import os

# Create static/ics directory if not exists
os.makedirs('static/ics', exist_ok=True)

# City coordinates for weather
CITIES = {
    'Beijing': {'lat': 39.9042, 'lon': 116.4074, 'name': '北京'},
    'Shanghai': {'lat': 31.2304, 'lon': 121.4737, 'name': '上海'},
    'Guangzhou': {'lat': 23.1291, 'lon': 113.2644, 'name': '广州'},
    'Shenzhen': {'lat': 22.5431, 'lon': 114.0579, 'name': '深圳'},
    'Hangzhou': {'lat': 30.2741, 'lon': 120.1551, 'name': '杭州'},
    'Ningbo': {'lat': 29.8683, 'lon': 121.5440, 'name': '宁波'},
    'Chengdu': {'lat': 30.5728, 'lon': 104.0668, 'name': '成都'},
    'Wuhan': {'lat': 30.5928, 'lon': 114.3055, 'name': '武汉'},
}

def generate_weather_calendar(city='Ningbo', days=7):
    # Use open-meteo API (free, no key)
    city_info = CITIES.get(city, CITIES['Ningbo'])
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city_info['lat']}&longitude={city_info['lon']}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Shanghai&forecast_days={days}"
    response = requests.get(url)
    data = response.json()
    if 'daily' not in data:
        print("API response:", data)
        raise ValueError("Daily data not found in API response")
    
    cal = Calendar()
    cal.add('prodid', f'-//{city_info["name"]}天气日历//')
    cal.add('version', '2.0')
    
    # Weather code mapping
    weather_map = {
        0: '☀️ 晴天', 1: '🌤️ 晴朗', 2: '⛅ 多云', 3: '☁️ 阴天',
        45: '🌫️ 雾', 48: '🌫️ 雾凇',
        51: '🌦️ 小雨', 53: '🌧️ 中雨', 55: '🌧️ 大雨',
        61: '🌧️ 小雨', 63: '🌧️ 中雨', 65: '⛈️ 大雨',
        71: '🌨️ 小雪', 73: '🌨️ 中雪', 75: '❄️ 大雪',
        80: '🌦️ 阵雨', 81: '⛈️ 强阵雨', 82: '⛈️ 暴雨',
        95: '⛈️ 雷暴', 96: '⛈️ 冰雹', 99: '⛈️ 强雷暴'
    }
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        temp_max = data['daily']['temperature_2m_max'][i]
        temp_min = data['daily']['temperature_2m_min'][i]
        weather_code = data['daily']['weathercode'][i]
        
        weather_desc = weather_map.get(weather_code, '🌡️ 未知')
        
        event = Event()
        event.add('summary', f"{city_info['name']} {weather_desc} {int(temp_min)}°C ~ {int(temp_max)}°C")
        event.add('dtstart', date.date())
        event.add('dtend', (date + timedelta(days=1)).date())
        event.add('description', f'{city_info["name"]}天气预报\n最低温度: {int(temp_min)}°C\n最高温度: {int(temp_max)}°C\n天气: {weather_desc}')
        cal.add_component(event)
    
    with open(f'static/ics/weather_{city}.ics', 'wb') as f:
        f.write(cal.to_ical())
    print(f"Generated weather calendar for {city_info['name']}")

def generate_holidays_calendar():
    # Chinese holidays for 2026
    holidays = [
        {'date': '2026-01-01', 'name': '🎆 元旦', 'days': 1},
        {'date': '2026-02-17', 'name': '🧧 春节（初一）', 'days': 7},
        {'date': '2026-04-05', 'name': '🌸 清明节', 'days': 1},
        {'date': '2026-05-01', 'name': '⚒️ 劳动节', 'days': 5},
        {'date': '2026-06-22', 'name': '🐉 端午节', 'days': 3},
        {'date': '2026-10-01', 'name': '🎊 国庆节', 'days': 7},
        {'date': '2026-10-26', 'name': '🥮 中秋节', 'days': 3},
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//中国节假日//')
    cal.add('version', '2.0')
    
    for h in holidays:
        event = Event()
        event.add('summary', h['name'])
        start_date = datetime.fromisoformat(h['date']).date()
        event.add('dtstart', start_date)
        event.add('dtend', start_date + timedelta(days=h['days']))
        event.add('description', f'法定节假日，共{h["days"]}天')
        cal.add_component(event)
    
    with open('static/ics/holidays.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated holidays calendar")

# Add more functions for lunar, zodiac, countdown

def generate_countdown_calendar():
    """生成重要日期倒计时"""
    countdowns = [
        {'date': '2026-06-07', 'name': '📚 2026年高考', 'emoji': '🎓'},
        {'date': '2026-12-26', 'name': '📝 2027年考研', 'emoji': '📖'},
        {'date': '2026-02-14', 'name': '💝 情人节', 'emoji': '💕'},
        {'date': '2026-12-25', 'name': '🎄 圣诞节', 'emoji': '🎅'},
        {'date': '2026-10-31', 'name': '🎃 万圣节', 'emoji': '👻'},
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//重要日期倒计时//')
    cal.add('version', '2.0')
    
    today = datetime.now().date()
    
    for cd in countdowns:
        target_date = datetime.fromisoformat(cd['date']).date()
        days_left = (target_date - today).days
        
        if days_left >= 0:  # Only add future events
            event = Event()
            event.add('summary', f"{cd['emoji']} {cd['name']} (还有{days_left}天)")
            event.add('dtstart', target_date)
            event.add('dtend', target_date + timedelta(days=1))
            event.add('description', f'距离{cd["name"]}还有 {days_left} 天')
            cal.add_component(event)
    
    with open('static/ics/countdown.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated countdown calendar")

def generate_weekly_reminder():
    """生成每周提醒事件"""
    cal = Calendar()
    cal.add('prodid', '-//每周提醒//')
    cal.add('version', '2.0')
    
    reminders = [
        {'day': 0, 'name': '💼 周一工作日', 'desc': '新的一周开始，加油！'},
        {'day': 4, 'name': '🎉 周五快乐', 'desc': '周末即将到来！'},
        {'day': 6, 'name': '😴 周日休息', 'desc': '好好休息，为新的一周做准备'},
    ]
    
    # Generate for next 12 weeks
    today = datetime.now().date()
    for week in range(12):
        for reminder in reminders:
            # Calculate the date
            days_ahead = reminder['day'] - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            target_date = today + timedelta(days=days_ahead + week * 7)
            
            event = Event()
            event.add('summary', reminder['name'])
            event.add('dtstart', target_date)
            event.add('dtend', target_date + timedelta(days=1))
            event.add('description', reminder['desc'])
            cal.add_component(event)
    
    with open('static/ics/weekly_reminder.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated weekly reminder calendar")

def generate_lunar_festivals():
    """生成传统农历节日（2026年）"""
    lunar_festivals = [
        {'date': '2026-02-17', 'name': '🧧 春节（正月初一）'},
        {'date': '2026-03-03', 'name': '🏮 元宵节（正月十五）'},
        {'date': '2026-05-19', 'name': '🐉 端午节（五月初五）'},
        {'date': '2026-08-19', 'name': '💝 七夕节（七月初七）'},
        {'date': '2026-10-06', 'name': '🥮 中秋节（八月十五）'},
        {'date': '2026-10-24', 'name': '👴 重阳节（九月初九）'},
        {'date': '2026-12-22', 'name': '🍜 冬至'},
        {'date': '2027-01-15', 'name': '🥟 腊八节（腊月初八）'},
        {'date': '2027-02-04', 'name': '🧨 小年（腊月廿三）'},
        {'date': '2027-02-05', 'name': '🧹 除夕（腊月廿九）'},
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//中国传统节日//')
    cal.add('version', '2.0')
    
    for festival in lunar_festivals:
        event = Event()
        event.add('summary', festival['name'])
        date_obj = datetime.fromisoformat(festival['date']).date()
        event.add('dtstart', date_obj)
        event.add('dtend', date_obj + timedelta(days=1))
        event.add('description', f'中国传统农历节日 - {festival["name"]}')
        cal.add_component(event)
    
    with open('static/ics/lunar_festivals.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated lunar festivals calendar")

if __name__ == '__main__':
    # Generate weather for multiple cities
    for city in ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Ningbo', 'Chengdu', 'Wuhan']:
        try:
            generate_weather_calendar(city)
        except Exception as e:
            print(f"Error generating weather for {city}: {e}")
    
    # Generate other calendars
    generate_holidays_calendar()
    generate_countdown_calendar()
    generate_weekly_reminder()
    generate_lunar_festivals()
    
    print("\n✅ All ICS files generated successfully!")