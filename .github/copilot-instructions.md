# Copilot Instructions

## Project Overview

A Python-based calendar subscription service that generates ICS files for weather forecasts, Chinese holidays/festivals, and reminders. Files are deployed as static assets to GitHub Pages and regenerated daily via a scheduled GitHub Actions workflow.

## Build & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Generate all ICS files
python3 generate.py

# Generate a specific type
python3 generate.py --type weather
python3 generate.py --type holidays
python3 generate.py --type reminders

# Generate weather for specific cities
python3 generate.py --type weather --cities Beijing Shanghai
```

There is no test suite. The primary validation is running `python3 generate.py` and confirming ICS files appear in `static/ics/`.

## Architecture

The pipeline is purely generative — no web server is used at runtime. `generate.py` is the entry point; it orchestrates all generators and outputs `.ics` files to `static/ics/`, which are then served statically via GitHub Pages.

```
generate.py  →  generators/*  →  static/ics/*.ics
                     ↑
              utils/calendar_helper.py (BaseCalendarGenerator)
              config/ (cities, holidays data, settings)
```

**Key flow:**
- `generate.py` imports all generator classes and calls `.generate()` or `.generate_and_save()` on each
- All generators inherit from `BaseCalendarGenerator` in `utils/calendar_helper.py`
- Weather data is fetched live from the [Open-Meteo API](https://open-meteo.com/) — no API key required
- Holiday and reminder data is static, defined in `config/holidays.py`

## Key Conventions

### Adding a new generator
Subclass `BaseCalendarGenerator`, implement `generate()`, and call `self.add_event(...)` then `self.save('filename.ics')`. Register the class in `generators/__init__.py` and wire it into `generate.py`.

```python
from utils import BaseCalendarGenerator

class MyGenerator(BaseCalendarGenerator):
    def __init__(self):
        super().__init__('My Calendar Name')

    def generate(self):
        self.add_event(
            summary='Event Title',
            start_date='2026-01-01',   # YYYY-MM-DD string or datetime.date
            description='Details'
        )
        self.save('my_calendar.ics')
```

### Adding a city
Edit `config/cities.py` with `lat`, `lon`, and Chinese `name`. The city key (e.g., `'Hangzhou'`) is used as the CLI argument and the output filename prefix (`weather_Hangzhou.ics`).

### Adding holidays/festivals
Append tuples of `(name, 'YYYY-MM-DD', description)` to the relevant list in `config/holidays.py`.

### Output path
All ICS files go to `static/ics/` (configured in `config/settings.py` as `OUTPUT_DIR`). The directory is auto-created on import.

### CI/CD
The GitHub Actions workflow (`.github/workflows/deploy.yml`) runs a Gitleaks security scan before building. It triggers on push to `main` and on a daily schedule (UTC 16:00 = Beijing midnight). Output is deployed to the `gh-pages` branch via `peaceiris/actions-gh-pages`.
