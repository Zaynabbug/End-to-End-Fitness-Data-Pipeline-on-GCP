WITH raw_data AS (
    SELECT 
        user_id,
        steps,
        distance_km,
        heart_rate,
        calories_burned,
        activity_type,
        workout_duration_min,
        TIMESTAMP(timestamp) AS event_time
    FROM `fit-analytics-pipeline.fitness_data.fitness_metrics`
)
SELECT 
    user_id,
    AVG(steps) AS avg_steps,
    AVG(distance_km) AS avg_distance_km,
    AVG(heart_rate) AS avg_heart_rate,
    SUM(calories_burned) AS total_calories,
    AVG(workout_duration_min) AS avg_workout_duration,
    DATE(event_time) AS activity_date
FROM raw_data
GROUP BY user_id, activity_date
