
# Dodawanie nowego serwera
INSERT_SERVER = '''INSERT INTO servers (name, ip_address, status, created_at)
VALUES ('app-server-01', '192.168.1.100', 'active', NOW())'''

# Dodawanie nowej metryki
INSERT_METRIC='''INSERT INTO metrics (server_id, cpu_usage, ram_usage, disk_io, net_io, timestamp)
VALUES (
  (SELECT id FROM servers WHERE name = 'app-server-01'),
  12.5,              -- cpu_usage (%)
  47.3,              -- ram_usage (%)
  1024.50,           -- disk_io (KB)
  256.00,            -- net_io (KB)
  NOW()
);'''
# Lista aktywnych serwerów z ich aktualnym użyciem CPU
UPDATE_SERVER='''UPDATE servers
SET status = 'inactive'
WHERE name = 'app-server-01';
'''
# Zmieniamy prog CPU z 70 na 80
UPDATE_THRESHOLDS='''UPDATE thresholds
SET threshold = 80.0
WHERE metric_type = 'cpu_usage'
  AND direction = 'above';
'''

# Serwery, które w ciągu ostatniej godziny przekroczyły próg CPU dla thresholds:
SELECT_FROM_SERVER='''SELECT
  s.id,
  s.name,
  s.ip_address,
  ROUND(AVG(m.cpu_usage), 2) AS avg_cpu_last5
FROM servers s
JOIN (
  SELECT *
  FROM metrics
  ORDER BY timestamp DESC
  LIMIT 5
) m ON m.server_id = s.id
WHERE s.status = 'active'
GROUP BY s.id, s.name, s.ip_address;
'''
# Statystyki historii alertów (ile alertów wygenerowalismy na każdy typ metryki)
SELECT_FROM_METRICS='''SELECT
  metric_type,
  COUNT(*) AS alerts_count,
  MIN(triggered_at) AS first_alert,
  MAX(triggered_at) AS last_alert
FROM alerts
GROUP BY metric_type
ORDER BY alerts_count DESC;
'''

# Łączenie danych z tabel JOINEM
SELECT_ALL='''SELECT
  s.name            AS server_name,
  m.cpu_usage,
  m.ram_usage,
  m.disk_io,
  m.net_io,
  m.timestamp
FROM metrics m
JOIN servers s ON s.id = m.server_id
ORDER BY m.timestamp DESC
LIMIT 50;
'''

# Listujemy wszystkie akcje skalowania serwerów z ich powodem

SELECT_ACTIONS='''SELECT
  sa.id AS action_id,
  s.name AS server_name,
  sa.action_type,
  sa.reason,
  sa.timestamp
FROM scale_actions sa
LEFT JOIN servers s ON s.id = sa.server_id
ORDER BY sa.timestamp DESC;
'''