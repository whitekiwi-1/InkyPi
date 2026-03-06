# Plugin Settings Persistence

## Overview
InkyPi now supports **persistent plugin settings storage**. Any configuration you enter in a plugin's settings form will be automatically saved to `device.json` and persist across:
- Page reloads
- Service restarts
- Device reboots

## How It Works

### 1. **Saving Settings**
When you visit a plugin's configuration page and click **"Save Settings"**, your configuration is:
- Sent to the `/save_plugin_settings` endpoint
- Stored in the `plugin_settings` section of `device.json`
- Persisted to disk permanently

### 2. **Loading Settings**
When you visit a plugin's configuration page, the form automatically:
- Fetches saved settings from the `/api/get_plugin_settings/<plugin_id>` endpoint
- Pre-populates all fields with your previously saved values
- Displays visual feedback (✓ or ✗) when loading is complete

### 3. **Using Settings in Plugins**
Your plugin's Python code can access the saved settings via:

```python
def generate_image(self, settings, device_config):
    # Get latitude/longitude from saved settings
    latitude = settings.get('latitude', '0')
    longitude = settings.get('longitude', '0')
    
    # Get calendar URLs (comes as a list)
    calendar_urls = settings.get('calendarURLs[]', [])
    if isinstance(calendar_urls, str):
        calendar_urls = [calendar_urls]
    
    # Use the settings...
```

## Weather Calendar Example

### Configuration Form
The `weather_calendar` plugin now includes:
- **Latitude** field (decimal, e.g., `40.7128`)
- **Longitude** field (decimal, e.g., `-74.0060`)
- **Temperature Units** dropdown (`metric` or `imperial`)
- **Calendar URLs** input (multiple iCloud .ics URLs supported)
- **Save Settings** button

### Form Features
✅ Auto-loads previously saved settings on page load  
✅ Displays "Settings saved successfully" confirmation  
✅ Shows error messages if something goes wrong  
✅ Supports adding multiple calendar URLs  

### Accessing Saved Settings

Your saved configuration is stored in `/opt/inkypi/src/config/device.json`:

```json
{
  "plugin_settings": {
    "weather_calendar": {
      "latitude": "40.499396",
      "longitude": "-3.863497",
      "units": "metric",
      "calendarURLs[]": [
        "https://p183-caldav.icloud.com/...",
        "https://p183-caldav.icloud.com/..."
      ]
    }
  }
}
```

## For Plugin Developers

### Creating a Settings Form
Create a `settings.html` file in your plugin directory:

```html
<form id="myPluginSettingsForm">
    <input type="hidden" name="plugin_id" value="my_plugin">
    
    <div class="settings-group">
        <label for="myField">My Setting</label>
        <input type="text" id="myField" name="myField" required>
    </div>
    
    <button type="submit" class="btn-primary">Save Settings</button>
</form>

<script>
    // Auto-load saved settings
    document.addEventListener('DOMContentLoaded', function() {
        fetch('/api/get_plugin_settings/my_plugin')
            .then(r => r.json())
            .then(data => {
                if (data.success && data.settings) {
                    document.getElementById('myField').value = data.settings.myField || '';
                }
            })
            .catch(e => console.log('No saved settings'));
    });
    
    // Handle form submission
    document.getElementById('myPluginSettingsForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        fetch('/save_plugin_settings', {
            method: 'POST',
            body: new FormData(this)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                alert('Settings saved!');
            } else {
                alert('Error: ' + data.error);
            }
        });
    });
</script>
```

### Backend Endpoints
Two new endpoints are now available:

#### `POST /save_plugin_settings`
Saves plugin configuration to `device.json`.

**Request:**
```
POST /save_plugin_settings
Content-Type: application/x-www-form-urlencoded

plugin_id=weather_calendar&latitude=40.7128&longitude=-74.0060&units=metric&calendarURLs[]=...
```

**Response:**
```json
{
  "success": true,
  "message": "Settings saved for weather_calendar"
}
```

#### `GET /api/get_plugin_settings/<plugin_id>`
Retrieves saved settings for a plugin.

**Request:**
```
GET /api/get_plugin_settings/weather_calendar
```

**Response:**
```json
{
  "success": true,
  "settings": {
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "units": "metric",
    "calendarURLs[]": ["https://..."]
  }
}
```

## Implementation Details

### Changes Made
1. **`src/blueprints/plugin.py`**
   - Added `save_plugin_settings()` endpoint (POST)
   - Added `get_plugin_settings()` endpoint (GET)
   - Both endpoints handle the `plugin_settings` dict in `device.json`

2. **`src/plugins/weather_calendar/settings.html`**
   - Added form submission handler
   - Added settings loader on page load
   - Added visual feedback (✓/✗) for save operations
   - Added "Save Settings" button

### Storage Format
Settings are stored in the `plugin_settings` object of `device.json`:

```json
{
  "device_name": "My Inky Display",
  "resolution": [800, 480],
  "plugin_settings": {
    "plugin_id": {
      "field1": "value1",
      "field2": "value2"
    }
  }
}
```

Each plugin gets its own key (the plugin ID) containing a dictionary of its settings.

## Troubleshooting

### Settings Not Saving?
1. Check browser console (F12) for JavaScript errors
2. Check InkyPi logs: `ssh inkypi "sudo journalctl -u inkypi -n 20 --no-pager"`
3. Verify `device.json` permissions: `ssh inkypi "ls -la /opt/inkypi/src/config/device.json"`

### Settings Lost After Restart?
This shouldn't happen. If it does:
1. Check that the settings were saved in `device.json`
2. Verify the plugin code is reading from the correct location
3. Ensure `device.json` has write permissions

### Form Not Pre-Populating?
1. Clear browser cache
2. Check that settings were previously saved
3. Verify the plugin_id matches between form and settings storage

## Testing

To test the persistence feature:

1. **Open the Weather Calendar settings:**
   ```
   http://your-inky-ip/plugin/weather_calendar
   ```

2. **Enter configuration:**
   - Latitude: `40.7128`
   - Longitude: `-74.0060`
   - Calendar URLs: paste your iCloud URL

3. **Click "Save Settings"** → Should see "✓ Settings saved successfully"

4. **Reload the page** → Fields should be pre-populated with your values

5. **Restart the service:**
   ```bash
   ssh inkypi "sudo systemctl restart inkypi"
   ```

6. **Reload the page again** → Settings should still be there!

## Next Steps

- Settings are now persisted automatically
- You can configure the plugin once and forget about it
- Settings survive restarts and reboots
- Ready for fine-tuning the visual appearance in the next phase
