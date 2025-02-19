WITH cleaned_data AS (
    SELECT
        user_id,
        steps,
        distance_km,
        heart_rate,
        calories_burned,
        activity_type,
        workout_duration_min,
        TIMESTAMP(timestamp) AS event_time
    FROM {{ source('fitness_data', 'fitness_metrics') }}
),
enriched_data AS (
    SELECT
        user_id,
        steps,
        distance_km,
        heart_rate,
        calories_burned,
        activity_type,
        workout_duration_min,
        event_time,
        -- Add derived columns
        CASE
            WHEN heart_rate < 70 THEN 'low'
            WHEN heart_rate BETWEEN 70 AND 120 THEN 'moderate'
            WHEN heart_rate > 120 THEN 'high'
        END AS intensity_level,
        -- Add a column for calories burned per minute
        ROUND(calories_burned / NULLIF(workout_duration_min, 0), 2) AS calories_per_minute
    FROM cleaned_data
)
SELECT *
FROM enriched_data