WITH ComparableRows AS (
    SELECT
        id, event_time, event_type, product_id, price, user_id, user_session,
        LAG(event_time, 1, NULL) OVER (ORDER BY event_time) AS previous_etime,
        LAG(event_type, 1, NULL) OVER (ORDER BY event_time) AS previous_etype,
        LAG(product_id, 1, NULL) OVER (ORDER BY event_time) AS previous_pid,
        LAG(price, 1, NULL) OVER (ORDER BY event_time) AS previous_price,
        LAG(user_id, 1, NULL) OVER (ORDER BY event_time) AS previous_uid,
        LAG(user_session, 1, NULL) OVER (ORDER BY event_time) AS previous_session
    FROM
        customers
),
Duplicates AS (
    SELECT
        id
    FROM
        ComparableRows
    WHERE
        previous_etime IS NOT NULL
        AND ABS(EXTRACT(EPOCH FROM (event_time - previous_etime))) <= 1
        AND event_type = previous_etype
        AND product_id = previous_pid
        AND price = previous_price
        AND user_id = previous_uid
        AND user_session = previous_session
)
DELETE FROM customers
WHERE id IN (SELECT id FROM Duplicates);

-- IDs 37 and 38 are duplicates and IDs 42 and 43 aswell
-- time psql -h localhost -U gcorreia -d piscineds -a -f remove_duplicates.sql
