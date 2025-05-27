-- IDs 37 and 38 are duplicates and IDs 42 and 43 aswell
-- time psql -h localhost -U gcorreia -d piscineds -a -f remove_duplicates.sql

WITH PotentialDuplicates AS (
    SELECT
        id,
        event_time,
        LAG(event_time, 1, NULL) OVER (PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_time) AS previous_etime,
        LAG(id, 1, NULL) OVER (PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_time) AS previous_id
    FROM
        customers
),
Duplicates AS (
    SELECT
        id
    FROM
        PotentialDuplicates
    WHERE
        previous_etime IS NOT NULL
        AND ABS(EXTRACT(EPOCH FROM (event_time - previous_etime))) <= 1
)
DELETE FROM customers
WHERE id IN (SELECT id FROM Duplicates);
