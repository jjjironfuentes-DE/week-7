
{% macro check_daily_revenue() %}

    {% set validation_query %}
        SELECT
            COUNT(*) AS ROW_COUNT,
            MAX(SALE_DATE) AS LATEST_SALE_DATE,
            IFF(
                MAX(SALE_DATE) <= CURRENT_DATE(),
                TRUE,
                FALSE
            ) AS DATE_IS_VALID
        FROM {{ target.database }}.{{ target.schema }}.DAILY_REVENUE
    {% endset %}

    {% set results = run_query(validation_query) %}

    {% if execute %}

        {% set row_count = results.columns[0].values()[0] | int %}
        {% set latest_date = results.columns[1].values()[0] %}
        {% set date_is_valid = results.columns[2].values()[0] | string | lower %}

        {% if row_count == 0 %}
            {{ exceptions.raise_compiler_error(
                "Validation failed: DAILY_REVENUE is empty."
            ) }}
        {% endif %}

        {% if latest_date is none or date_is_valid != 'true' %}
            {{ exceptions.raise_compiler_error(
                "Validation failed: latest sale date is invalid."
            ) }}
        {% endif %}

        {{ log(
            "DAILY_REVENUE validation passed. Rows: " ~ row_count
            ~ ", latest sale date: " ~ latest_date,
            info=True
        ) }}

    {% endif %}

{% endmacro %}

# DAILY_REVENUE validation passed.
# Rows: 381
# latest sale date: 2025-03-23
