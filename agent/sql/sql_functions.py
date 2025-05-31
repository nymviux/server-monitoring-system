


# Zwraca średnie zużycie CPU dla danego serwera
GET_AVG_CPU_FN='''CREATE OR REPLACE FUNCTION get_avg_cpu(server_id INT)
RETURNS NUMERIC(5,2) AS $$
BEGIN
    RETURN (
        SELECT ROUND(AVG(cpu_usage), 2)
        FROM metrics
        WHERE server_id = get_avg_cpu.server_id
    );
END;
$$ LANGUAGE plpgsql;'''

# Zwraca ostatnie metryki dla danego serwera
GET_METRICS_FN='''CREATE OR REPLACE FUNCTION get_latest_metrics(p_server_id INT)
RETURNS TABLE(cpu NUMERIC, ram NUMERIC, disk NUMERIC, net NUMERIC, ts TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT cpu_usage, ram_usage, disk_io, net_io, timestamp
    FROM metrics
    WHERE server_id = p_server_id
    ORDER BY timestamp DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;'''


# Dodaje metrykę do serwera
INSERT_METRICS_FN='''CREATE OR REPLACE PROCEDURE insert_metric(
    p_server_id INT,
    p_cpu NUMERIC,
    p_ram NUMERIC,
    p_disk NUMERIC,
    p_net NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO metrics(server_id, cpu_usage, ram_usage, disk_io, net_io)
    VALUES (p_server_id, p_cpu, p_ram, p_disk, p_net);
END;
$$;'''

# Automatyczna aktualizacja statusu serwer na "inactive",
#  jeśli nie ma metryk z ostatniej godziny.
ACT_STATUS_FN='''CREATE OR REPLACE PROCEDURE deactivate_inactive_servers()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE servers
    SET status = 'inactive'
    WHERE id NOT IN (
        SELECT DISTINCT server_id
        FROM metrics
        WHERE timestamp > now() - INTERVAL '1 hour'
    );
END;
$$;'''