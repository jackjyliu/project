SELECT p.ts, p.power_use_mwh, w.temp_c, w.rel_hum_pct, w.pressure_kpa, r.rain_mm,
        EXTRACT(YEAR FROM p.ts)::text AS year,
        EXTRACT(MONTH FROM p.ts)::text AS month,
        EXTRACT(ISODOW FROM p.ts)::text AS day_of_week,
        EXTRACT(HOUR FROM p.ts)::text as hour,
        CASE 
            WHEN p.ts + INTERVAL '30 minutes' BETWEEN d.rise AND d.set THEN 1
            ELSE 0
        END is_daylight,
        CASE
            WHEN h.hdate IS NULL THEN 0
            ELSE 1
        END is_holiday

FROM power AS p
LEFT JOIN daylight AS d ON date_trunc('day', p.ts) = date_trunc('day', d.cdate)
LEFT JOIN weather AS w ON p.ts = w.ts
LEFT JOIN rain as r ON p.ts = r.ts
LEFT JOIN holiday as h ON date_trunc('day', p.ts) = date_trunc('day', h.hdate)
ORDER BY p.ts