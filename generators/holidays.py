"""Holiday calendar generators."""

from datetime import datetime
from utils import BaseCalendarGenerator
from config import HOLIDAYS_2026, LUNAR_FESTIVALS, SOLAR_TERMS, INTERNATIONAL_HOLIDAYS


class HolidaysGenerator(BaseCalendarGenerator):
    """Generate Chinese public holidays calendar."""
    
    def __init__(self):
        super().__init__('中国法定节假日')
    
    def generate(self):
        """Generate holidays calendar."""
        for name, start, end in HOLIDAYS_2026:
            self.add_event(
                summary=name,
                start_date=start,
                end_date=end,
                description=f'{name} - 中国法定节假日'
            )
        self.save('holidays.ics')


class LunarFestivalsGenerator(BaseCalendarGenerator):
    """Generate lunar festivals calendar."""
    
    def __init__(self):
        super().__init__('中国传统节日')
    
    def generate(self):
        """Generate lunar festivals calendar."""
        for name, date, desc in LUNAR_FESTIVALS:
            self.add_event(
                summary=name,
                start_date=date,
                description=desc
            )
        self.save('lunar_festivals.ics')


class SolarTermsGenerator(BaseCalendarGenerator):
    """Generate 24 solar terms calendar."""
    
    def __init__(self):
        super().__init__('二十四节气')
    
    def generate(self):
        """Generate solar terms calendar."""
        for name, date, desc in SOLAR_TERMS:
            self.add_event(
                summary=f'{name} - 二十四节气',
                start_date=date,
                description=desc
            )
        self.save('solar_terms.ics')


class InternationalHolidaysGenerator(BaseCalendarGenerator):
    """Generate international holidays calendar."""
    
    def __init__(self):
        super().__init__('国际节日')
    
    def generate(self):
        """Generate international holidays calendar."""
        for name, date, desc in INTERNATIONAL_HOLIDAYS:
            self.add_event(
                summary=name,
                start_date=date,
                description=desc
            )
        self.save('international_holidays.ics')
