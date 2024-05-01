{{ config(materialized="view") }}

SELECT * FROM {{ source('shiny_data', 'packages') }}
