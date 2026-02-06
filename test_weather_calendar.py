#!/usr/bin/env python3
"""
Quick test script to verify weather_calendar plugin loads and generates image
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from plugins.weather_calendar.weather_calendar import WeatherCalendar
from config import Config
import json
from datetime import datetime

def test_plugin():
    print("🧪 Testing Weather Calendar Plugin...\n")
    
    # Load config
    config = Config()
    device_config = config
    
    # Plugin settings
    settings = {
        'latitude': '40.7128',
        'longitude': '-74.0060',
        'units': 'metric',
        'calendarURLs[]': []
    }
    
    # Create plugin instance
    plugin_config = {
        'id': 'weather_calendar',
        'class': 'WeatherCalendar',
        'display_name': 'Weather + Calendar'
    }
    
    try:
        plugin = WeatherCalendar(plugin_config)
        print("✅ Plugin initialized successfully")
        
        # Try to generate image
        print("📡 Fetching weather data from Open-Meteo...")
        image = plugin.generate_image(settings, device_config)
        
        if image:
            print("✅ Image generated successfully!")
            print(f"   Image size: {image.size}")
            
            # Save to mock display output
            os.makedirs('mock_display_output', exist_ok=True)
            image.save('mock_display_output/weather_test.png')
            print(f"💾 Saved to: mock_display_output/weather_test.png")
            
            return True
        else:
            print("❌ Image generation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_plugin()
    sys.exit(0 if success else 1)
