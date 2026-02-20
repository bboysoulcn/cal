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

def generate_solar_terms():
    """生成24节气日历（2026年）"""
    solar_terms = [
        {'date': '2026-01-05', 'name': '🌨️ 小寒', 'desc': '天气渐寒，开始进入一年中最冷的时段'},
        {'date': '2026-01-20', 'name': '❄️ 大寒', 'desc': '一年中最冷的时期'},
        {'date': '2026-02-04', 'name': '🌱 立春', 'desc': '春季的开始，万物复苏'},
        {'date': '2026-02-19', 'name': '🌧️ 雨水', 'desc': '降雨开始，雨量渐增'},
        {'date': '2026-03-05', 'name': '⚡ 惊蛰', 'desc': '春雷始鸣，蛰虫惊醒'},
        {'date': '2026-03-20', 'name': '⚖️ 春分', 'desc': '昼夜平分，春季过半'},
        {'date': '2026-04-04', 'name': '🌸 清明', 'desc': '天气清明，踏青扫墓'},
        {'date': '2026-04-20', 'name': '🌾 谷雨', 'desc': '雨生百谷，播种时节'},
        {'date': '2026-05-05', 'name': '☀️ 立夏', 'desc': '夏季开始，气温升高'},
        {'date': '2026-05-21', 'name': '🌿 小满', 'desc': '麦类作物开始饱满'},
        {'date': '2026-06-05', 'name': '🌾 芒种', 'desc': '麦类收获，稻类播种'},
        {'date': '2026-06-21', 'name': '🌞 夏至', 'desc': '白昼最长，夏季过半'},
        {'date': '2026-07-07', 'name': '🌡️ 小暑', 'desc': '天气炎热，但不到极点'},
        {'date': '2026-07-22', 'name': '🔥 大暑', 'desc': '一年中最热的时期'},
        {'date': '2026-08-07', 'name': '🍂 立秋', 'desc': '秋季开始，暑去凉来'},
        {'date': '2026-08-23', 'name': '🌾 处暑', 'desc': '暑气渐消，秋意渐浓'},
        {'date': '2026-09-07', 'name': '🌫️ 白露', 'desc': '天气转凉，露水增多'},
        {'date': '2026-09-23', 'name': '⚖️ 秋分', 'desc': '昼夜平分，秋季过半'},
        {'date': '2026-10-08', 'name': '🍁 寒露', 'desc': '露水寒冷，将要结冰'},
        {'date': '2026-10-23', 'name': '❄️ 霜降', 'desc': '天气渐冷，开始降霜'},
        {'date': '2026-11-07', 'name': '🍃 立冬', 'desc': '冬季开始，万物收藏'},
        {'date': '2026-11-22', 'name': '🌨️ 小雪', 'desc': '开始降雪，但雪量不大'},
        {'date': '2026-12-07', 'name': '❄️ 大雪', 'desc': '降雪量增多，地面积雪'},
        {'date': '2026-12-21', 'name': '🌙 冬至', 'desc': '白昼最短，冬季过半'},
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//24节气//')
    cal.add('version', '2.0')
    
    for term in solar_terms:
        event = Event()
        event.add('summary', term['name'])
        date_obj = datetime.fromisoformat(term['date']).date()
        event.add('dtstart', date_obj)
        event.add('dtend', date_obj + timedelta(days=1))
        event.add('description', term['desc'])
        cal.add_component(event)
    
    with open('static/ics/solar_terms.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated solar terms calendar")

def generate_international_holidays():
    """生成国际节日日历"""
    holidays = [
        {'date': '2026-01-01', 'name': '🎆 元旦', 'desc': 'New Year\'s Day'},
        {'date': '2026-02-14', 'name': '💝 情人节', 'desc': 'Valentine\'s Day'},
        {'date': '2026-03-08', 'name': '👩 国际妇女节', 'desc': 'International Women\'s Day'},
        {'date': '2026-04-01', 'name': '😄 愚人节', 'desc': 'April Fools\' Day'},
        {'date': '2026-04-05', 'name': '🌍 世界卫生日', 'desc': 'World Health Day'},
        {'date': '2026-04-22', 'name': '🌎 世界地球日', 'desc': 'Earth Day'},
        {'date': '2026-05-01', 'name': '⚒️ 国际劳动节', 'desc': 'International Workers\' Day'},
        {'date': '2026-05-10', 'name': '💐 母亲节', 'desc': 'Mother\'s Day (5月第2个周日)'},
        {'date': '2026-06-01', 'name': '👶 国际儿童节', 'desc': 'International Children\'s Day'},
        {'date': '2026-06-21', 'name': '👨 父亲节', 'desc': 'Father\'s Day (6月第3个周日)'},
        {'date': '2026-07-11', 'name': '🌍 世界人口日', 'desc': 'World Population Day'},
        {'date': '2026-08-08', 'name': '🐱 国际猫咪日', 'desc': 'International Cat Day'},
        {'date': '2026-09-10', 'name': '👨‍🏫 教师节', 'desc': 'Teachers\' Day (中国)'},
        {'date': '2026-09-21', 'name': '☮️ 国际和平日', 'desc': 'International Day of Peace'},
        {'date': '2026-10-01', 'name': '👴 国际老年人日', 'desc': 'International Day of Older Persons'},
        {'date': '2026-10-24', 'name': '🌍 联合国日', 'desc': 'United Nations Day'},
        {'date': '2026-10-31', 'name': '🎃 万圣节', 'desc': 'Halloween'},
        {'date': '2026-11-26', 'name': '🦃 感恩节', 'desc': 'Thanksgiving Day (11月第4个周四)'},
        {'date': '2026-12-24', 'name': '🎄 平安夜', 'desc': 'Christmas Eve'},
        {'date': '2026-12-25', 'name': '🎅 圣诞节', 'desc': 'Christmas Day'},
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//国际节日//')
    cal.add('version', '2.0')
    
    for holiday in holidays:
        event = Event()
        event.add('summary', holiday['name'])
        date_obj = datetime.fromisoformat(holiday['date']).date()
        event.add('dtstart', date_obj)
        event.add('dtend', date_obj + timedelta(days=1))
        event.add('description', holiday['desc'])
        cal.add_component(event)
    
    with open('static/ics/international_holidays.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated international holidays calendar")

def generate_health_reminders():
    """生成健康提醒日历"""
    cal = Calendar()
    cal.add('prodid', '-//健康提醒//')
    cal.add('version', '2.0')
    
    # 每周健康提醒
    health_tips = [
        {'day': 0, 'name': '💧 多喝水提醒', 'desc': '每天喝8杯水，保持身体水分'},
        {'day': 1, 'name': '🏃 运动日', 'desc': '坚持运动30分钟，保持健康体魄'},
        {'day': 2, 'name': '🥗 健康饮食', 'desc': '多吃蔬菜水果，少油少盐'},
        {'day': 3, 'name': '😊 保持好心情', 'desc': '心理健康同样重要，保持乐观心态'},
        {'day': 4, 'name': '👀 护眼提醒', 'desc': '远离电子屏幕，保护眼睛'},
        {'day': 5, 'name': '🧘 放松休息', 'desc': '适当放松，劳逸结合'},
        {'day': 6, 'name': '😴 早睡早起', 'desc': '保证充足睡眠，晚上11点前入睡'},
    ]
    
    # Generate for next 12 weeks
    today = datetime.now().date()
    for week in range(12):
        for tip in health_tips:
            days_ahead = tip['day'] - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            target_date = today + timedelta(days=days_ahead + week * 7)
            
            event = Event()
            event.add('summary', tip['name'])
            event.add('dtstart', target_date)
            event.add('dtend', target_date + timedelta(days=1))
            event.add('description', tip['desc'])
            cal.add_component(event)
    
    with open('static/ics/health_reminders.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated health reminders calendar")

def generate_financial_calendar():
    """生成财经日历"""
    # 2026年重要财经日期
    financial_events = [
        {'date': '2026-01-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-02-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-03-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-03-15', 'name': '📊 个税申报截止', 'desc': '年度个人所得税汇算清缴'},
        {'date': '2026-04-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-05-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-06-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-06-30', 'name': '💼 半年总结', 'desc': '上半年财务回顾与规划'},
        {'date': '2026-07-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-08-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-09-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-10-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-11-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-11-11', 'name': '🛒 双十一购物节', 'desc': '理性消费，避免冲动购物'},
        {'date': '2026-12-10', 'name': '💰 发薪日提醒', 'desc': '本月工资发放日（具体以公司为准）'},
        {'date': '2026-12-12', 'name': '🛒 双十二购物节', 'desc': '理性消费，避免冲动购物'},
        {'date': '2026-12-31', 'name': '📈 年度总结', 'desc': '年度财务回顾与下年规划'},
    ]
    
    cal = Calendar()
    cal.add('prodid', '-//财经日历//')
    cal.add('version', '2.0')
    
    for event_data in financial_events:
        event = Event()
        event.add('summary', event_data['name'])
        date_obj = datetime.fromisoformat(event_data['date']).date()
        event.add('dtstart', date_obj)
        event.add('dtend', date_obj + timedelta(days=1))
        event.add('description', event_data['desc'])
        cal.add_component(event)
    
    with open('static/ics/financial_calendar.ics', 'wb') as f:
        f.write(cal.to_ical())
    print("Generated financial calendar")

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
    generate_solar_terms()
    generate_international_holidays()
    generate_health_reminders()
    generate_financial_calendar()
    
    print("\n✅ All ICS files generated successfully!")