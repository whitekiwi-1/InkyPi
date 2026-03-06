# Display Clarity Test & Optimization

## What Changed?

Your Weather Calendar template has been **optimized for e-ink display clarity**:

### Key Improvements:
✅ **Pure black & white only** (removed grays)  
✅ **Bolder, larger text** (font-weight 700-900)  
✅ **Thicker borders** (2px → 3px)  
✅ **Better spacing** (more padding)  
✅ **No rounded corners** (sharper edges)  
✅ **Anti-aliasing optimized** for crisp rendering  

## Test the Changes

### Quick Test (Immediate Visual Check)

1. **Wait for next automatic refresh** (top of the hour, every 1 hour)
   - Or manually trigger an update:
   ```bash
   ssh inkypi "curl -X POST http://localhost/update_now \
     -d 'plugin_id=weather_calendar&latitude=40.7128&longitude=-74.0060&units=metric'"
   ```

2. **Check if display is sharper/clearer:**
   - Look at text sharpness (dates, temperatures, event times)
   - Check contrast between text and background
   - Verify borders are crisp and defined

### What to Look For

**Before Optimization:**
- Soft gray backgrounds (`#f8f8f8`)
- Blue/red colored text
- Thin borders (2px)
- Gray divider lines
- Overall may look slightly "washed out"

**After Optimization:**
- Pure white backgrounds with pure black text
- **Much higher contrast** - text should pop
- Bold, prominent borders (3px)
- Clear separation between elements
- Should look **sharper and more crisp**

## If Display Still Doesn't Look Crisp

Here are some debugging steps:

### 1. Check Service is Running
```bash
ssh inkypi "sudo systemctl status inkypi | head -10"
```

Should show: `Active: active (running)`

### 2. Verify Latest Code is Loaded
```bash
ssh inkypi "cat /opt/inkypi/src/plugins/weather_calendar/render/weather_calendar.html | grep 'font-weight: 900' | head -1"
```

Should return: A line with `font-weight: 900`

If not, the code wasn't pulled. Try:
```bash
ssh inkypi "cd /opt/inkypi && sudo git pull origin main"
```

### 3. Force Manual Update
```bash
ssh inkypi "curl -X POST http://localhost/update_now \
  -d 'plugin_id=weather_calendar' \
  -d 'latitude=40.7128' \
  -d 'longitude=-74.0060' \
  -d 'units=metric'"
```

Wait 30 seconds, then check the display.

### 4. Check Generated Image
View the PNG that was generated:
```bash
ssh inkypi "ls -lh /opt/inkypi/src/static/images/plugins/weather_calendar/*.png | tail -1"
```

Copy it to your Mac to inspect:
```bash
scp inkypi:/opt/inkypi/src/static/images/plugins/weather_calendar/latest.png \
  ~/Desktop/weather_calendar_latest.png
```

Then open in Preview to check clarity.

### 5. Check Service Logs
```bash
ssh inkypi "sudo journalctl -u inkypi -n 30 --no-pager | tail -30"
```

Look for any error messages. Should see:
```
weather_calendar plugin executing with settings...
Image already displayed, skipping refresh
```

## Fine-Tuning the Display

If the display is **too light**, **too dark**, or you want to adjust:

### Option 1: Increase Contrast Further

Edit the template on your Mac:
```bash
nano /Users/pablojuanes/Documents/InkyPi/src/plugins/weather_calendar/render/weather_calendar.html
```

Find this section:
```css
.forecast-card {
    border: 3px solid #000;
    padding: 20px;
    background-color: #fff;
}
```

Change to:
```css
.forecast-card {
    border: 4px solid #000;     /* Thicker border */
    padding: 24px;              /* More padding */
    background-color: #fff;
}
```

### Option 2: Make Text Bigger

Find:
```css
.forecast-card .date {
    font-size: 18px;
    font-weight: 900;
}
```

Change to:
```css
.forecast-card .date {
    font-size: 20px;        /* Bigger */
    font-weight: 900;
}
```

### Option 3: Add Color Accents

If you want to experiment with color (Inky Impression supports red):

```css
.forecast-card .temps .max {
    color: #FF0000;  /* Pure red for max temps */
    font-weight: 900;
}
```

After any changes:
```bash
cd /Users/pablojuanes/Documents/InkyPi
git add -A
git commit -m "tune: adjust display appearance"
git push mi-fork main

# Then on Raspberry Pi:
ssh inkypi "cd /opt/inkypi && sudo git pull origin main && sudo systemctl restart inkypi"
```

## Understanding E-Ink Rendering

Your Pimoroni Inky Impression Spectra is a **7-color e-ink display**:
- White (background)
- Black (text, borders)
- Red (accents)
- Yellow (accents)
- Blue (can dither)
- Orange (can dither)
- Mixed (dithering)

**Important:** E-ink dislikes:
- ❌ Light gray colors (become dithered/grainy)
- ❌ Thin lines (become blurry)
- ❌ Small text (hard to read)
- ❌ Rounded corners (pixelate)

E-ink loves:
- ✅ Pure black/white (crisp)
- ✅ Bold, thick elements
- ✅ Large, heavy fonts
- ✅ High contrast
- ✅ Simple, clean design

## Next Steps

1. **Look at your display** - Is it sharper now?
2. **If yes** 🎉 - You can now fine-tune colors/layout
3. **If no** - Let's investigate further (display settings, rendering pipeline, etc.)

The changes should be immediately visible. If you don't see improvement within 1-2 hours of the change, something may not have updated correctly.

## Troubleshooting Checklist

- [ ] Service is running: `systemctl status inkypi`
- [ ] Latest code is pulled: Check for `font-weight: 900` in HTML
- [ ] Service was restarted: `systemctl restart inkypi`
- [ ] Enough time passed: 1-2 hours for automatic refresh
- [ ] Manual update was triggered: Used the `curl` command above
- [ ] Generated image was checked: Looked at PNG file on Mac

If all checks pass but still not sharp, let me know and we'll investigate:
- Chrome screenshot settings
- Image enhancement settings in device.json
- Display settings on the Pimoroni hardware
- Possible hardware issue
