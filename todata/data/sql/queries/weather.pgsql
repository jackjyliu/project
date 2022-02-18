SELECT 
    t.ts,
    w.temp_c, w.rel_hum_pct, w.pressure_kpa, w.rain_mm,
    EXTRACT(YEAR FROM t.ts)::int AS year,
        EXTRACT(MONTH FROM t.ts)::int AS month,
        EXTRACT(ISODOW FROM t.ts)::int AS day_of_week,
        EXTRACT(HOUR FROM t.ts)::int as hour,
        CASE 
            WHEN t.ts + INTERVAL '30 minutes' BETWEEN d.rise AND d.set THEN 1
            ELSE 0
        END is_daylight,
        CASE
            WHEN h.hdate IS NULL THEN 0
            ELSE 1
        END is_holiday

FROM   (SELECT 
            date_trunc('hour', ts)::timestamp as ts
        FROM
            generate_series
        ( '2021-01-01 00:00:00'::timestamp 
        , '2021-12-31 23:00:00	'::timestamp
        , '1 hour'::interval) ts
        ) as t

LEFT JOIN dt_daylight AS d ON date_trunc('day', t.ts) = date_trunc('day', d.cdate)
LEFT JOIN weather_temperature AS w ON t.ts = w.ts
LEFT JOIN dt_holiday as h ON date_trunc('day', t.ts) = date_trunc('day', h.hdate)
ORDER BY t.ts