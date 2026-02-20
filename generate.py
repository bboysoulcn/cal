#!/usr/bin/env python3
"""
Calendar Subscription Service Generator
Generate various ICS calendar files for subscription.
"""

import sys
import argparse
from generators import (
    WeatherGenerator,
    HolidaysGenerator,
    LunarFestivalsGenerator,
    SolarTermsGenerator,
    InternationalHolidaysGenerator,
    CountdownGenerator,
    WeeklyReminderGenerator,
    HealthRemindersGenerator,
    FinancialCalendarGenerator,
)
from config import CITIES


def generate_weather_calendars(cities=None):
    """
    Generate weather calendars for specified cities.
    
    Args:
        cities: List of city keys, or None for all cities
    """
    if cities is None:
        cities = list(CITIES.keys())
    
    print(f"\n📍 Generating weather calendars for {len(cities)} cities...")
    
    generator = WeatherGenerator()
    for city in cities:
        generator.generate_and_save(city)


def generate_holiday_calendars():
    """Generate all holiday-related calendars."""
    print("\n🎊 Generating holiday calendars...")
    
    HolidaysGenerator().generate()
    LunarFestivalsGenerator().generate()
    SolarTermsGenerator().generate()
    InternationalHolidaysGenerator().generate()


def generate_reminder_calendars():
    """Generate all reminder calendars."""
    print("\n⏰ Generating reminder calendars...")
    
    CountdownGenerator().generate()
    WeeklyReminderGenerator().generate()
    HealthRemindersGenerator().generate()
    FinancialCalendarGenerator().generate()


def generate_all():
    """Generate all calendars."""
    print("=" * 60)
    print("🗓️  Calendar Subscription Service Generator")
    print("=" * 60)
    
    try:
        generate_weather_calendars()
        generate_holiday_calendars()
        generate_reminder_calendars()
        
        print("\n" + "=" * 60)
        print("✅ All ICS files generated successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point with command line argument support."""
    parser = argparse.ArgumentParser(
        description='Generate ICS calendar files for subscription service'
    )
    
    parser.add_argument(
        '--type',
        choices=['all', 'weather', 'holidays', 'reminders'],
        default='all',
        help='Type of calendars to generate (default: all)'
    )
    
    parser.add_argument(
        '--cities',
        nargs='+',
        choices=list(CITIES.keys()),
        help='Cities for weather calendars (default: all)'
    )
    
    args = parser.parse_args()
    
    if args.type == 'all':
        generate_all()
    elif args.type == 'weather':
        generate_weather_calendars(args.cities)
    elif args.type == 'holidays':
        generate_holiday_calendars()
    elif args.type == 'reminders':
        generate_reminder_calendars()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # No arguments provided, generate all
        generate_all()
    else:
        # Parse command line arguments
        main()
