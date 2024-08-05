{{config(alias='gold_sc_clubs_age') }}
SELECT 
    COUNT(1) foundation_year_count,
    EXTRACT(year from DATE(foundation_date)) as foundation_year
FROM 
    {{ source('public', 'bronze_sc_teams') }}
WHERE EXTRACT(year from DATE(foundation_date)) is not null
GROUP BY foundation_year
ORDER BY foundation_year ASC
