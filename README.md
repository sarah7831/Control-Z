# Control-Z
Real-Time Traffic Analytics
🚦 Real-Time Traffic Monitoring System

Azure IoT Hub | Stream Analytics | SQL Database | Power BI

This project provides a real-time traffic monitoring pipeline using Azure services. It ingests streaming traffic data, processes it using Azure Stream Analytics, stores it in Azure SQL Database, and visualizes it through Power BI with real-time dashboards.

📌 Project Architecture
Traffic Data Source → Azure Stream Analytics → Azure SQL Database → Power BI Dashboard

#✨ Features

✔ Real-time traffic ingestion

✔ Stream processing using Azure Stream Analytics

✔ Data storage in Azure SQL Database

✔ Interactive Power BI dashboard

✔ Filtering by region, speed, incidents, etc.

✔ Optional alerts via Azure Monitor or Power BI

✔ Landing page with KPIs and daily summary

✔ Supports testing & production modes

#🧩 Technologies Used
Component	Technology
Data Source	Simulated traffic events
Stream Processing	Azure Stream Analytics
Storage	Azure SQL Database
Visualization	Power BI Desktop / Power BI Service
Alerts	Azure Monitor (recommended)
Optional	Logic Apps for email notifications
📥 Data Schema (Azure SQL Database)
CREATE TABLE [LiveTrafficData] (
    [region] nvarchar(4000),
    [latitude] float,
    [longitude] float,
    [EventProcessedUtcTime] datetime2,
    [temperature_c] float,
    [humidity_pct] bigint,
    [wind_speed_m_s] float,
    [current_speed_kmph] bigint,
    [free_flow_speed_kmph] bigint,
    [current_travel_time_sec] bigint,
    [num_traffic_incidents] bigint,
    [feels_like_c] float,
    [free_flow_travel_time_sec] bigint,
    [confidence] float,
    [road_closed] nvarchar(4000)
);

#⚙️ Stream Analytics Query
SELECT 
    region,
    lat AS latitude,
    lon AS longitude,
    System.Timestamp() AS EventProcessedUtcTime,
    temperature AS temperature_c,
    humidity AS humidity_pct,
    wind_speed AS wind_speed_m_s,
    current_speed AS current_speed_kmph,
    free_flow_speed AS free_flow_speed_kmph,
    travel_time AS current_travel_time_sec,
    incidents_count AS num_traffic_incidents,
    CAST(NULL AS FLOAT) AS feels_like_c,
    CAST(NULL AS BIGINT) AS free_flow_travel_time_sec,
    CAST(NULL AS FLOAT) AS confidence,
    CAST(NULL AS NVARCHAR(MAX)) AS road_closed
INTO
    [SQLOutput]
FROM
    traffictestt;

#📊 Power BI Dashboard

Your dashboard includes:

📍 Real-time map view (if enabled by admin)

#▶️ How to Run the Project
1. Start Data Simulation

Send traffic events to your input source (IoT Hub/Event Hub).

2. Run Stream Analytics Job

Input: traffic stream

Output: Azure SQL Database

3. Connect Power BI

Power BI Service → Get Data → Azure SQL DB → Enter credentials

4. Refresh Dashboard

Scheduled refresh every 15 min
(Real-time tiles work instantly for DirectQuery)




Add road-closure prediction model

Add historical trend warehouse (Azure Synapse)

Add APIs for external apps
