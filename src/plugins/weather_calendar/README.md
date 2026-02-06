# Weather + Calendar Plugin

Combine a 3-day weather forecast with today's iCloud calendar events in one beautiful display.

## Features

- **3-Day Weather Forecast**: Shows temperature range, weather conditions for today and next 2 days
- **Today's Events**: Displays all calendar events for today from your iCloud calendars
- **Free Weather API**: Uses Open-Meteo (no API key required)
- **Multiple Calendars**: Support for multiple iCloud calendar URLs
- **Customizable**: Temperature units (Celsius/Fahrenheit), custom title

## Requirements

- **Latitude & Longitude**: Your location coordinates
- **iCloud Calendar URLs** (optional): Public .ics URLs from your iCloud calendars

## Getting iCloud Calendar URLs

1. Open **iCloud.com** → Calendar
2. Right-click on a calendar → **Share Settings**
3. Click **"Share Calendar"** to enable sharing
4. Copy the **Public Calendar Link** (ends in `.ics`)
5. Paste it into the plugin settings

## Settings

| Setting | Description | Required |
|---------|-------------|----------|
| **Title** | Custom display title | No |
| **Latitude** | Your location latitude (decimal) | Yes |
| **Longitude** | Your location longitude (decimal) | Yes |
| **Temperature Units** | Celsius or Fahrenheit | Yes |
| **iCloud Calendar URLs** | Public .ics URLs from iCloud | No |

## Example Configuration

```json
{
  "customTitle": "My Weather & Schedule",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "units": "imperial",
  "calendarURLs[]": [
    "https://p12-caldav.icloud.com/..../calendar.ics"
  ]
}
```

## Notes

- Weather data updates every hour (from Open-Meteo API)
- Calendar events sync based on your InkyPi refresh schedule
- No API keys needed for weather data
- Handles all-day events and timed events automatically
- Events are sorted by start time

## Troubleshooting

**No events showing?**
- Verify the calendar is shared publicly in iCloud settings
- Check that the .ics URL is correct and accessible
- Ensure events are on today's date

**Weather not updating?**
- Verify latitude/longitude are correct
- Check that network connectivity is available
- Open-Meteo API is free and reliable — if issues persist, check their status page

**Display not fitting?**
- Adjust font sizes in CSS if needed
- Consider reducing number of calendars or title length
