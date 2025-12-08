# 🚦 Real-Time Traffic Monitoring System

> **Monitor Cairo's traffic flow in real-time using Azure Cloud Services**

A comprehensive traffic analytics pipeline that ingests live traffic and weather data, processes it through Azure Stream Analytics, stores it in a SQL database, and visualizes insights through interactive Power BI dashboards.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Project Components](#-project-components)
- [Configuration](#-configuration)
- [Dashboard](#-dashboard)
- [Future Enhancements](#-future-enhancements)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

This project provides a **real-time traffic monitoring solution** for Cairo's major regions. It combines:
- Live traffic flow data from TomTom API
- Weather conditions from OpenWeatherMap API
- Incident reporting and alerts
- Real-time visualization and analytics

**Perfect for:** Traffic management centers, urban planning, logistics companies, or anyone interested in real-time IoT data pipelines.

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐     ┌─────────────────────┐
│  Python Script  │────▶│  Azure Event Hub │────▶│ Stream Analytics    │
│ (Data Ingestion)│      │ (Data Ingestion) │     │  (Data Processing)  │
└─────────────────┘      └──────────────────┘     └─────────────────────┘
         │                                                    │
         ▼                                                    ▼
┌─────────────────┐                              ┌─────────────────────┐
│  External APIs  │                              │  Azure SQL Database │
│  • TomTom       │                              │  (Data Storage)     │
│  • OpenWeather  │                              └─────────────────────┘
└─────────────────┘                                          │
                                                             ▼
                                                  ┌─────────────────────┐
                                                  │      Power BI       │
                                                  │   (Visualization)   │
                                                  └─────────────────────┘
```

### Data Flow
1. **Collection:** Python script queries APIs every 60 seconds for 6 Cairo regions
2. **Ingestion:** Data streams into Azure Event Hub as JSON messages
3. **Processing:** Stream Analytics transforms and standardizes the data
4. **Storage:** Cleaned data is stored in Azure SQL Database
5. **Visualization:** Power BI dashboards display real-time insights

---

## ✨ Features

### Core Capabilities
- ✅ **Real-time data ingestion** from multiple API sources
- ✅ **Automated stream processing** with Azure Stream Analytics
- ✅ **Scalable storage** in Azure SQL Database
- ✅ **Interactive dashboards** with Power BI
- ✅ **Multi-region monitoring** (6 Cairo locations)
- ✅ **Weather correlation analysis**
- ✅ **Incident tracking** (accidents, road closures)

### Analytics Features
- 📊 Traffic speed vs. free-flow speed comparison
- 🌡️ Weather impact on traffic patterns
- 🚨 Real-time incident alerts
- 📍 Geographic heatmaps
- ⏱️ Travel time analysis
- 📈 Historical trend visualization

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Data Collection** | Python  | API integration & data generation |
| **Streaming Ingestion** | Azure Event Hub | High-throughput message broker |
| **Stream Processing** | Azure Stream Analytics | Real-time data transformation |
| **Data Storage** | Azure SQL Database | Structured data warehouse |
| **Visualization** | Power BI Desktop/Service | Interactive dashboards |
| **APIs** | TomTom Traffic API | Traffic flow & incidents |
| | OpenWeatherMap API | Weather data |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Azure subscription (with credits or free tier)
- API keys for TomTom and OpenWeatherMap
- Power BI Desktop (free download)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/sarah7831/Control-Z.git
cd traffic-analytics
```

#### 2. Install Python Dependencies
```bash
pip install azure-eventhub requests
```

#### 3. Configure API Keys
Edit the Python script and add your credentials:
```python
OWM_KEY = "your_openweathermap_api_key"
TOMTOM_KEY = "your_tomtom_api_key"
EVENT_HUB_CONNECTION = "your_event_hub_connection_string"
EVENT_HUB_NAME = "your_event_hub_name"
```

#### 4. Set Up Azure Resources

**Create Event Hub:**
```bash
# Via Azure Portal or CLI
az eventhubs namespace create --name traffic-hub --resource-group myResourceGroup
az eventhubs eventhub create --name traffic-events --namespace-name traffic-hub
```

**Create SQL Database:**
- Use the provided `database_schema.sql` to create the table
- Note the connection string for Stream Analytics

**Configure Stream Analytics:**
- Create a new Stream Analytics job
- Set Event Hub as input
- Set SQL Database as output
- Paste the provided query from `stream_analytics_query.sql`

#### 5. Run the Data Generator
```bash
python traffic_data_generator.py
```

You should see output like:
```
Connected to Azure Event Hub. Streaming data...
Sent: Downtown | Speed 15 km/h | Incidents 2
Sent: Nasr City | Speed 45 km/h | Incidents 0
```

#### 6. Connect Power BI
- Open Power BI Desktop
- Get Data → Azure SQL Database
- Enter your database credentials
- Import the `LiveTrafficData` table
- Build your dashboard or use the provided template

---

## 📦 Project Components

### 1. Data Generator (`traffic_data_generator.py`)
**Purpose:** Continuously fetches traffic and weather data from APIs

**Key Functions:**
- `get_weather(lat, lon)` - Retrieves weather conditions
- `get_traffic_flow(lat, lon)` - Gets current traffic speed
- `get_traffic_incidents(lat, lon)` - Checks for accidents/closures

**Monitored Regions:**
- Downtown Cairo
- Nasr City
- New Cairo
- Maadi
- Heliopolis
- Mokattam

### 2. Database Schema (`database_schema.sql`)
**Table:** `LiveTrafficData`

**Key Columns:**
- `region` - Location name
- `latitude`, `longitude` - GPS coordinates
- `EventProcessedUtcTime` - Timestamp (indexed for fast queries)
- `temperature_c`, `humidity_pct`, `wind_speed_m_s` - Weather metrics
- `current_speed_kmph` - Actual traffic speed
- `free_flow_speed_kmph` - Normal speed (no congestion)
- `num_traffic_incidents` - Count of accidents/issues

### 3. Stream Analytics Query (`stream_analytics_query.sql`)
**Transformations:**
- Renames fields to match database schema
- Adds processing timestamp
- Handles null values for future features
- Converts data types appropriately

---

## ⚙️ Configuration

### Monitored Regions
Edit in `traffic_data_generator.py`:
```python
CAIRO_REGIONS = {
    "Downtown": (30.0444, 31.2357),
    "Your Region": (latitude, longitude)
}
```

### Data Collection Interval
Default: 60 seconds. Modify in the script:
```python
time.sleep(60)  # Change to desired seconds
```

### Stream Analytics Window
For aggregations, modify the query:
```sql
SELECT 
    region,
    AVG(current_speed_kmph) as avg_speed
FROM traffictestt
GROUP BY region, TumblingWindow(minute, 5)  -- 5-minute windows
```

---

## 📊 Dashboard

### Power BI Setup

**Refresh Options:**
1. **Scheduled Refresh:** Every 15 minutes (for historical charts)
2. **DirectQuery:** Real-time tiles update instantly

**Recommended Visuals:**
- 🗺️ **Map:** Plot regions with color-coded congestion levels
- 📈 **Line Chart:** Speed trends over time
- 📊 **Bar Chart:** Incidents by region
- 🌡️ **Scatter Plot:** Temperature vs. traffic speed correlation
- 🔢 **KPI Cards:** Current average speed, total incidents, active regions

### Sample DAX Measures
```dax
Congestion Level = 
    IF(
        [current_speed_kmph] < [free_flow_speed_kmph] * 0.5,
        "High",
        IF([current_speed_kmph] < [free_flow_speed_kmph] * 0.8, "Medium", "Low")
    )

Delay Minutes = 
    ([current_travel_time_sec] - [free_flow_travel_time_sec]) / 60
```

---

## 🔮 Future Enhancements

### Planned Features
- [ ] **Machine Learning Model** - Predict road closures using historical patterns
- [ ] **Azure Synapse Integration** - Long-term data warehousing for trend analysis
- [ ] **Public REST API** - Allow external apps to query traffic data
- [ ] **Mobile App** - iOS/Android interface for commuters
- [ ] **Alert System** - SMS/email notifications for severe congestion
- [ ] **Expanded Coverage** - Add more Egyptian cities

### Potential Improvements
- Add route optimization suggestions
- Integrate public transportation data
- Implement anomaly detection for unusual traffic patterns
- Create predictive models for rush hour patterns

---

## 🐛 Troubleshooting

### Common Issues

**Problem:** "Connection refused to Event Hub"
```
Solution: Check connection string format and firewall rules
Verify: az eventhubs namespace show --name your-namespace
```

**Problem:** Stream Analytics job not starting
```
Solution: Ensure input/output are properly configured
Check: Test connection in Stream Analytics portal
```

**Problem:** No data appearing in SQL Database
```
Solution: 
1. Check Stream Analytics query syntax
2. Verify SQL credentials in output settings
3. Check if Python script is running
4. Review Stream Analytics error logs
```

**Problem:** Power BI not refreshing
```
Solution:
1. Check gateway connection (if using on-premises)
2. Verify SQL firewall allows Power BI IPs
3. Use DirectQuery mode for real-time data
```

### Logs & Monitoring
- **Event Hub Metrics:** Azure Portal → Your Event Hub → Metrics
- **Stream Analytics:** Job → Activity Log / Diagnostic Settings
- **SQL Database:** Query Performance Insights

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

---

## 👥 Team

This project was developed by a team of 5 contributors:
- Abd El-Hakim Abdelaziz
- Ahmed Mostafa Ellaboudy
- Sarah Mohamed
- Wessal Osama
- Shahd Mohamed


### Team Contributions
- **Collaborative Design:** Architecture planning and technology selection
- **Code Reviews:** Peer review process for quality assurance
- **Testing:** End-to-end testing across all pipeline stages
- **Documentation:** Comprehensive project documentation and guides

---

## 📧 Contact
- **Project Repository:** https://github.com/sarah7831/Control-Z.git
- **Issues & Feedback:** Use GitHub Issues tab

---

## 🙏 Acknowledgments
- TomTom for traffic API
- OpenWeatherMap for weather data
- Microsoft Azure for cloud infrastructure
- **Special thanks** to our professors and mentors for guidance throughout this project

---

**⭐ If you find this project helpful, please star the repository!**

Last Updated: December 2025
