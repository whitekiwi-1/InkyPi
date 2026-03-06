# Testing Settings Persistence

## Quick Test (2 minutes)

1. **Open the Weather Calendar settings page:**
   ```
   http://your-inky-ip:8080/plugin/weather_calendar
   ```
   (Replace `your-inky-ip` with your Raspberry Pi's IP address)

2. **Fill in some values:**
   - Latitude: `40.7128`
   - Longitude: `-74.0060`
   - Temperature Units: Choose `metric` or `imperial`
   - Calendar URL: Leave empty for now (or paste an iCloud URL if you have one)

3. **Click "Save Settings"**
   - You should see: **✓ Settings saved successfully** (green checkmark)
   - Wait 2-3 seconds, the message will disappear

4. **Reload the page** (F5 or Cmd+R)
   - The form fields should be **pre-populated** with your saved values
   - This means settings were saved to `device.json`!

5. **Verify settings persisted on the device:**
   ```bash
   ssh inkypi "cat /opt/inkypi/src/config/device.json | grep -A 10 'plugin_settings'"
   ```
   
   You should see something like:
   ```json
   "plugin_settings": {
       "weather_calendar": {
           "latitude": "40.7128",
           "longitude": "-74.0060",
           "units": "metric"
       }
   }
   ```

## Extended Test (5 minutes)

1. **Restart the InkyPi service:**
   ```bash
   ssh inkypi "sudo systemctl restart inkypi"
   ```

2. **Wait 10 seconds** for the service to come back up

3. **Reload the page again**
   - The form should still have your saved values!
   - This proves the settings survived the restart

4. **Test adding multiple calendar URLs:**
   - Click "+ Add Another Calendar" button
   - Enter your iCloud calendar URLs
   - Click "Save Settings"
   - Reload the page
   - All URLs should still be there

## What Changed

### New Endpoints
```
POST /save_plugin_settings          → Save plugin config to device.json
GET  /api/get_plugin_settings/<id>  → Load plugin config from device.json
```

### Form Improvements
- ✓ "Save Settings" button (was missing before)
- ✓ Auto-loads saved values on page load
- ✓ Shows success/error messages
- ✓ Settings persist across restarts

### Storage Location
Settings are stored in: `/opt/inkypi/src/config/device.json`

Under the `plugin_settings` object:
```json
{
  "plugin_settings": {
    "weather_calendar": {
      "latitude": "40.499396",
      "longitude": "-3.863497",
      "units": "metric",
      "calendarURLs[]": [...]
    },
    "other_plugin": {...}
  }
}
```

## Troubleshooting

### "✗ Error: An error occurred"
- Check browser console (F12) for details
- Check server logs: `ssh inkypi "sudo journalctl -u inkypi -n 20 --no-pager"`

### Fields not pre-filling after reload
- Clear browser cache: Cmd+Shift+Delete (or Ctrl+Shift+Delete)
- Try a different browser
- Check `device.json` has correct values

### "Save Settings" button not appearing
- Clear browser cache
- Make sure service restarted: `ssh inkypi "sudo systemctl status inkypi"`

## Next Phase

Once you confirm settings are persisting correctly, we can move to the next refinements:
- Visual design improvements
- Layout optimization
- Color adjustments for your 7-color e-ink display
- Refresh timing adjustments
