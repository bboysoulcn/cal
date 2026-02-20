"""Calendar generation helper utilities."""

import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from config.settings import OUTPUT_DIR, TIMEZONE


class BaseCalendarGenerator:
    """Base class for all calendar generators."""
    
    def __init__(self, name):
        """
        Initialize calendar generator.
        
        Args:
            name: Calendar name for prodid
        """
        self.name = name
        self.calendar = Calendar()
        self.calendar.add('prodid', f'-//{name}//')
        self.calendar.add('version', '2.0')
    
    def add_event(self, summary, start_date, end_date=None, description=''):
        """
        Add an event to the calendar.
        
        Args:
            summary: Event title
            start_date: Start date (datetime or string YYYY-MM-DD)
            end_date: End date (optional, defaults to start_date)
            description: Event description
        """
        event = Event()
        event.add('summary', summary)
        
        # Parse dates if strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Default end_date to start_date
        if end_date is None:
            end_date = start_date
        
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        
        if description:
            event.add('description', description)
        
        self.calendar.add_component(event)
    
    def save(self, filename):
        """
        Save calendar to file.
        
        Args:
            filename: Output filename (without path)
        """
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(self.calendar.to_ical())
        print(f"✅ Generated: {filepath}")


def save_calendar(calendar, filename):
    """
    Save a calendar object to file.
    
    Args:
        calendar: icalendar Calendar object
        filename: Output filename (without path)
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(calendar.to_ical())
    print(f"✅ Generated: {filepath}")


def create_date_range(start_date, days):
    """
    Create a list of dates starting from start_date.
    
    Args:
        start_date: Starting date
        days: Number of days
        
    Returns:
        List of datetime objects
    """
    return [start_date + timedelta(days=i) for i in range(days)]


def parse_date(date_str):
    """
    Parse date string in YYYY-MM-DD format.
    
    Args:
        date_str: Date string
        
    Returns:
        datetime.date object
    """
    return datetime.strptime(date_str, '%Y-%m-%d').date()
