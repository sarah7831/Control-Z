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
    CAST(NULL AS NVARCHAR(max)) AS road_closed
INTO
    [sqltest]
FROM
    traffictestt;
