# E-Ink Display Optimization Guide

## Problem Identified

Your Pimoroni Inky Impression Spectra 7.3 display wasn't showing crisp/sharp content because the original template used:
- ❌ Soft grays (`#f8f8f8`, `#999`, `#ccc`) - Not ideal for e-ink
- ❌ Blue and red colors (`#1976d2`, `#d32f2f`) - Difficult on e-ink
- ❌ Anti-aliased fonts - Can look blurry on e-ink
- ❌ Low contrast overall

## Solutions Implemented

### 1. **Pure Black & White Only**
Changed from:
```css
background-color: #f8f8f8;  /* Soft gray */
color: #666;                /* Medium gray */
```

To:
```css
background-color: #fff;     /* Pure white */
color: #000;                /* Pure black */
```

**Why?** E-ink displays work best with high contrast. Gray colors can appear dithered or unclear.

### 2. **Bolder Typography**
Increased font weights for clarity:
- `font-weight: bold` → `font-weight: 700` and `font-weight: 900`
- Larger font sizes for important content
- Better line-height for readability

### 3. **Stronger Borders**
- Changed `border: 2px solid #000` → `border: 3px solid #000`
- Thicker divider lines (2px → 3px)
- Better visual separation on e-ink

### 4. **Anti-Aliasing Control**
Added CSS for crisp rendering:
```css
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

This prevents font blur on webkit/Firefox browsers.

### 5. **Better Letter Spacing**
Added `letter-spacing: 0.5px` to key elements for clarity:
- Dates: `letter-spacing: 0.5px`
- Times: `letter-spacing: 0.5px`
- Temperatures: `letter-spacing: 1px`

### 6. **Removed Rounded Corners**
- E-ink doesn't render curves smoothly
- Changed `border-radius: 5px` → Removed
- Keeps design sharp and crisp

### 7. **Increased Padding & Gaps**
- More breathing room between elements
- Less crowded layout
- Better readability on small screens

## Key Changes Summary

| Element | Before | After | Reason |
|---------|--------|-------|--------|
| Background | `#f8f8f8` gray | `#fff` white | Higher contrast |
| Text color | `#666` gray | `#000` black | Better visibility |
| Border width | 2px | 3px | More defined |
| Font weight | 500-bold | 600-900 | Sharper text |
| Card bg | Gray | White | Cleaner look |
| Border color | `#1976d2` blue | `#000` black | E-ink friendly |
| Padding | 18px | 20px | More space |

## Fine-Tuning Options

### If it's still too light/blurry:

1. **Increase border thickness further:**
   ```css
   .forecast-card {
       border: 4px solid #000;  /* Was 3px */
   }
   ```

2. **Make fonts even bolder:**
   ```css
   .forecast-card .date {
       font-weight: 950;  /* Was 900 */
   }
   ```

3. **Increase font sizes:**
   ```css
   .forecast-card .date {
       font-size: 20px;  /* Was 18px */
   }
   ```

### If you want to add subtle colors (Inky Impression supports Red, Yellow, Black, White):

You can use these colors, but only for accent elements:

```css
/* Option: Red accent for high temps */
.forecast-card .temps .max {
    color: #FF0000;  /* Pure red */
}

/* Option: Yellow accent for warnings */
.forecast-card .condition {
    color: #FFD700;  /* Pure yellow */
}
```

**Note:** Only use pure, saturated colors for e-ink displays. Avoid shades.

### If text is too crowded:

Increase line-height:
```css
.event-item .title {
    line-height: 1.5;  /* Was 1.3 */
}
```

## How to Test Changes Locally

### On Your Mac (Development Mode):

```bash
cd /Users/pablojuanes/Documents/InkyPi
python src/inkypi.py --dev
```

Then open: `http://localhost:8080/plugin/weather_calendar`

Click "Update Now" and check `mock_display_output/latest.png` to preview changes.

### On Raspberry Pi (Production):

After making changes:

```bash
cd /opt/inkypi
sudo git pull origin main
sudo systemctl restart inkypi
```

Then wait ~1 minute for the next scheduled refresh, or:

```bash
curl -X POST http://your-inky-ip/update_now -d 'plugin_id=weather_calendar&latitude=40.7128&longitude=-74.0060&units=metric'
```

## E-Ink Design Best Practices

### DO ✓
- ✅ Use pure black (`#000`) and white (`#fff`)
- ✅ Make text **bold** and **large**
- ✅ Use high contrast
- ✅ Use clean, simple fonts (Helvetica, Arial)
- ✅ Use thick borders and lines
- ✅ Use ample spacing and padding
- ✅ Limit text to essential information
- ✅ Use left-align or center-align

### DON'T ✗
- ❌ Use light grays or soft colors
- ❌ Use thin fonts or light font-weights
- ❌ Use gradients or complex shading
- ❌ Use rounded corners (they blur)
- ❌ Use drop shadows
- ❌ Use small fonts
- ❌ Crowd information together
- ❌ Use thin lines

## Performance Impact

These changes have **zero performance impact**:
- ✅ No additional API calls
- ✅ Same image generation time
- ✅ Same file size
- ✅ Same refresh interval (1 hour)

## Next Steps

1. **Review the changes** by looking at the rendered image on your display
2. **Fine-tune colors/sizes** if needed using the options above
3. **Test different conditions** (sunny, rainy, snowy forecasts)
4. **Compare with other displays** to ensure readability

The display should now appear **noticeably sharper and more readable** on your Inky Impression!
