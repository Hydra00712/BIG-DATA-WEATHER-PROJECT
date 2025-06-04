# 📊 How to Create the Weather Dashboard in Kibana

## 🎯 Goal: Recreate the Beautiful Multi-City Weather Dashboard

This guide will help you create the exact dashboard shown in your image with:
- Temperature trend lines for each city
- Current "Feels Like" temperature metrics
- Current humidity percentages
- Professional layout with 7 European cities

---

## 📋 Prerequisites
✅ Index pattern `openweather*` created in Kibana
✅ Weather data flowing (you should have this already!)
✅ At least 30-60 minutes of historical data for trend lines

---

## 🏗️ Step 1: Create Individual Visualizations

### A. Temperature Line Charts (6 charts needed)

**For each city (Krakow, Paris, Berlin, Amsterdam, Barcelona, Vienna):**

1. **Go to Visualize** → **Create visualization** → **Line**
2. **Select index**: `openweather*`
3. **Configure:**
   - **Y-axis (Metrics)**:
     - Aggregation: `Average`
     - Field: `temp`
     - Custom Label: `Average Temperature`
   
   - **X-axis (Buckets)**:
     - Aggregation: `Date Histogram`
     - Field: `@timestamp` or `created_at`
     - Interval: `Auto`
   
   - **Split Series (Buckets)**:
     - Sub Aggregation: `Terms`
     - Field: `city_name.keyword`
     - Size: 1
     - Include: `"Krakow"` (change for each city)

4. **Styling:**
   - Color: Green (#00D4AA)
   - Line width: 2px
   - Show dots: Yes

5. **Save as**: `Temperature Trend - Krakow`

**Repeat for all 6 cities**: Paris, Berlin, Amsterdam, Barcelona, Vienna

### B. "Feels Like" Metric Visualizations (6 metrics needed)

**For each city:**

1. **Go to Visualize** → **Create visualization** → **Metric**
2. **Select index**: `openweather*`
3. **Configure:**
   - **Metrics**:
     - Aggregation: `Top Hit`
     - Field: `feels_like`
     - Aggregate with: `Latest`
     - Size: 1
   
   - **Buckets** (Add filter):
     - Filter: `city_name.keyword:"Krakow"`

4. **Styling:**
   - Font size: Large
   - Show label: Yes
   - Custom label: `FEELS LIKE`

5. **Save as**: `Feels Like - Krakow`

**Repeat for all 6 cities**

### C. Humidity Metric Visualizations (6 metrics needed)

**Same as "Feels Like" but:**
- Field: `humidity`
- Custom label: `HUMIDITY`
- Save as: `Humidity - Krakow`

---

## 🎨 Step 2: Create the Dashboard

1. **Go to Dashboard** → **Create new dashboard**

2. **Add visualizations** in this layout:

```
┌─────────────────┬─────────────┬─────────────────┬─────────────┐
│ Temp - Krakow   │ Feels-Krakow│ Temp - Paris    │ Feels-Paris │
├─────────────────┼─────────────┼─────────────────┼─────────────┤
│ Humidity-Krakow │             │ Humidity-Paris  │             │
├─────────────────┼─────────────┼─────────────────┼─────────────┤
│ Temp - Berlin   │ Feels-Berlin│ Temp - Amsterdam│ Feels-Amst  │
├─────────────────┼─────────────┼─────────────────┼─────────────┤
│ Humidity-Berlin │             │ Humidity-Amst   │             │
├─────────────────┼─────────────┼─────────────────┼─────────────┤
│ Temp - Barcelona│ Feels-Barc  │ Temp - Vienna   │ Feels-Vienna│
├─────────────────┼─────────────┼─────────────────┼─────────────┤
│ Humidity-Barc   │             │ Humidity-Vienna │             │
└─────────────────┴─────────────┴─────────────────┴─────────────┘
```

3. **Resize panels** to match the image proportions

4. **Set time range**: Last 24 hours

5. **Enable auto-refresh**: Every 1 minute

6. **Save dashboard as**: `Weather Monitoring Dashboard`

---

## ⚡ Quick Alternative: Use Lens (Easier!)

If the above seems complex, try **Lens** (modern visualization):

1. **Go to Lens** → **Create visualization**
2. **Drag fields**:
   - X-axis: `@timestamp`
   - Y-axis: `temp`
   - Break down by: `city_name.keyword`
3. **Chart type**: Line
4. **Save and add to dashboard**

---

## 🎯 Pro Tips for Perfect Recreation

1. **Colors**: Use green (#00D4AA) for all temperature lines
2. **Grid**: 4 columns × 6 rows layout
3. **Spacing**: Minimal gaps between panels
4. **Time range**: Last 24 hours for best trend visibility
5. **Auto-refresh**: 1-minute intervals
6. **Panel titles**: City names in caps (KRAKOW, PARIS, etc.)

---

## 🔧 Troubleshooting

**No data showing?**
- Check if index pattern `openweather*` exists
- Verify time range includes your data
- Check field names match your data structure

**Lines not smooth?**
- Increase time range to get more data points
- Adjust date histogram interval

**Metrics showing wrong values?**
- Use "Top Hit" aggregation for latest values
- Verify field names (`feels_like`, `humidity`)

---

## 🚀 Next Steps

Once dashboard is created:
1. Set as default dashboard
2. Share with team
3. Set up alerts for extreme temperatures
4. Add more cities if needed

**Happy dashboarding! 📊✨**
