{{config(alias='gold_all_teams') }}
SELECT 
    team_name,
    DATE(foundation_date) as foundation_date,
    cnpj,
    stadium,
    colors,
    president_name,
    address,
    cep
FROM 
    {{ source('public', 'bronze_sc_teams') }}
ORDER BY 
    foundation_date desc