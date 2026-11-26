WITH source AS (

    SELECT *
    FROM {{ source('brewbeats', 'coffee_sales') }}

),

renamed AS (

    SELECT
        DATE AS sale_date,
        DATETIME AS sale_datetime,
        CASH_TYPE AS payment_type,
        CARD AS card_number,
        MONEY AS revenue,
        COFFEE_NAME AS coffee_name

    FROM source

)

SELECT *
FROM renamed