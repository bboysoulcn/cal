"""Configuration module for calendar service."""

from .cities import CITIES
from .holidays import HOLIDAYS_2026, LUNAR_FESTIVALS, SOLAR_TERMS, INTERNATIONAL_HOLIDAYS
from .settings import OUTPUT_DIR, TIMEZONE, WEATHER_API_URL

__all__ = [
    'CITIES',
    'HOLIDAYS_2026',
    'LUNAR_FESTIVALS',
    'SOLAR_TERMS',
    'INTERNATIONAL_HOLIDAYS',
    'OUTPUT_DIR',
    'TIMEZONE',
    'WEATHER_API_URL',
]
