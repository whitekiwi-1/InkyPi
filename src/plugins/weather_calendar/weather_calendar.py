from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import requests
import logging
from datetime import datetime, timedelta, timezone
import pytz
import icalendar
import recurring_ical_events

logger = logging.getLogger(__name__)

UNITS = {
    "metric": {
        "temperature": "°C",
        "speed": "m/s"
    },
    "imperial": {
        "temperature": "°F",
        "speed": "mph"
    }
}

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,precipitation,precipitation_probability,relative_humidity_2m,surface_pressure,visibility&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset&current_weather=true&timezone=auto&models=best_match&forecast_days=3"


class WeatherCalendar(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['style_settings'] = True
        template_params['calendar_settings'] = True
        return template_params

    def generate_image(self, settings, device_config):
        """
        Generate image combining weather forecast (3 days) + today's calendar events.
        """
        # Get weather data
        lat = settings.get('latitude')
        long = settings.get('longitude')
        if not lat or not long:
            raise RuntimeError("Latitude and Longitude are required.")

        units = settings.get('units', 'metric')
        if units not in ['metric', 'imperial']:
            raise RuntimeError("Units must be 'metric' or 'imperial'.")

        timezone_str = device_config.get_config("timezone", default="America/New_York")
        time_format = device_config.get_config("time_format", default="12h")
        tz = pytz.timezone(timezone_str)

        # Get weather forecast
        try:
            weather_data = self.get_open_meteo_data(lat, long)
        except Exception as e:
            logger.error(f"Weather API request failed: {str(e)}")
            raise RuntimeError("Failed to fetch weather data.")

        # Get calendar events for today
        calendar_urls = settings.get('calendarURLs[]', [])
        events_today = []
        
        if calendar_urls:
            try:
                events_today = self.fetch_calendar_events_today(calendar_urls, tz)
            except Exception as e:
                logger.error(f"Calendar fetch failed: {str(e)}")
                # Don't fail completely if calendar fails, just show weather

        # Parse weather data
        weather_info = self.parse_weather_data(weather_data, units, tz, time_format)

        # Prepare template params
        template_params = {
            "title": settings.get('customTitle', 'Weather & Today\'s Events'),
            "weather": weather_info,
            "events": events_today,
            "units": UNITS.get(units, UNITS['metric']),
            "timezone": timezone_str,
            "time_format": time_format,
            "plugin_settings": settings
        }

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        # Render HTML to image
        image = self.render_image(dimensions, "weather_calendar.html", "weather_calendar.css", template_params)
        
        if not image:
            raise RuntimeError("Failed to render image.")
        
        return image

    def get_open_meteo_data(self, lat, long):
        """Fetch weather data from Open-Meteo API (free, no API key needed)."""
        url = OPEN_METEO_FORECAST_URL.format(lat=lat, long=long)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def parse_weather_data(self, data, units, tz, time_format):
        """
        Parse Open-Meteo response into weather info for 3 days.
        Returns list of daily forecasts with temp, conditions, etc.
        """
        daily_data = data.get('daily', {})
        current_data = data.get('current_weather', {})
        
        weather_code_map = {
            0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Foggy", 48: "Foggy", 51: "Light Rain", 53: "Moderate Rain",
            55: "Heavy Rain", 61: "Rain", 63: "Heavy Rain", 65: "Very Heavy Rain",
            71: "Light Snow", 73: "Moderate Snow", 75: "Heavy Snow", 77: "Snow Grains",
            80: "Light Rain Showers", 81: "Moderate Rain Showers", 82: "Heavy Rain Showers",
            85: "Light Snow Showers", 86: "Heavy Snow Showers", 95: "Thunderstorm",
            96: "Thunderstorm with Hail", 99: "Thunderstorm with Hail"
        }
        
        forecasts = []
        
        times = daily_data.get('time', [])
        temps_max = daily_data.get('temperature_2m_max', [])
        temps_min = daily_data.get('temperature_2m_min', [])
        weather_codes = daily_data.get('weathercode', [])
        
        temp_unit = UNITS[units]['temperature']
        
        for i in range(min(3, len(times))):  # 3 days
            date_obj = datetime.fromisoformat(times[i])
            forecast = {
                "date": date_obj.strftime("%a, %b %d" if time_format == "24h" else "%a, %m/%d"),
                "day_name": date_obj.strftime("%A"),
                "temp_max": f"{int(temps_max[i])}",
                "temp_min": f"{int(temps_min[i])}",
                "condition": weather_code_map.get(weather_codes[i], "Unknown"),
                "temp_unit": temp_unit
            }
            forecasts.append(forecast)
        
        return forecasts

    def fetch_calendar_events_today(self, calendar_urls, tz):
        """
        Fetch events from iCloud calendar URLs (ICS format) for today.
        """
        events = []
        now = datetime.now(tz)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        for url in calendar_urls:
            if not url.strip():
                continue
                
            try:
                response = requests.get(url.strip(), timeout=10)
                response.raise_for_status()
                
                cal = icalendar.Calendar.from_ical(response.content)
                day_events = recurring_ical_events.of(cal).between(start_of_day, end_of_day)
                
                for event in day_events:
                    event_data = self.parse_event(event, tz)
                    if event_data:
                        events.append(event_data)
            except Exception as e:
                logger.warning(f"Failed to fetch calendar from {url}: {str(e)}")
                continue
        
        # Sort events by start time
        events.sort(key=lambda x: x['start_time'])
        
        return events

    def parse_event(self, event, tz):
        """Parse an icalendar event into dict with start_time, title, etc."""
        try:
            title = str(event.get('summary', 'Untitled'))
            dt_start = event.get('dtstart')
            
            if not dt_start:
                return None
            
            start = dt_start.dt
            
            # Handle all-day events and datetime objects
            if hasattr(start, 'time'):  # datetime object
                if start.tzinfo is None:
                    start = tz.localize(start)
                else:
                    start = start.astimezone(tz)
                start_time = start.strftime("%H:%M")
            else:  # date object
                start_time = "All day"
            
            return {
                "title": title,
                "start_time": start_time
            }
        except Exception as e:
            logger.warning(f"Failed to parse event: {str(e)}")
            return None
