-- Excursions
SELECT * FROM cold_chain_data
WHERE temperature < 2 OR temperature > 8;

-- Count by container
SELECT container_id, COUNT(*) AS excursions
FROM cold_chain_data
WHERE temperature < 2 OR temperature > 8
GROUP BY container_id;

-- Average by location
SELECT location, ROUND(AVG(temperature), 2) AS avg_temp
FROM cold_chain_data
GROUP BY location;
