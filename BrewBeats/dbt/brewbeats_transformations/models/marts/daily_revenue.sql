WITH coffee_sales AS (

    SELECT *
    FROM {{ ref('stg_coffee_sales') }}

),

daily_revenue AS (

    SELECT
        sale_date,
        COUNT(*) AS total_transactions,
        SUM(revenue) AS total_revenue

    FROM coffee_sales
    GROUP BY sale_date

)

SELECT *
FROM daily_revenue