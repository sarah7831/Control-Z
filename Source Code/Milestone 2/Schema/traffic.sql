
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
	-- Corrected data types for the NULL fields
	[feels_like_c] float,
	[free_flow_travel_time_sec] bigint,
	[confidence] float,
	[road_closed] nvarchar(4000)
)
CREATE CLUSTERED INDEX [ix_1] ON [LiveTrafficData]([EventProcessedUtcTime])
