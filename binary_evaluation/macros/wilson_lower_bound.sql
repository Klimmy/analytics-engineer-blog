{% macro wilson_lower_bound(p, n) %}

    {% set z = 1.96 %}
    {% set z_2 %}
    POW({{ z }}, 2)
    {% endset %}
    {% set p_cc %}
    GREATEST({{ p }} - 1 / (2 * {{ n }}), 0)
    {% endset %}

    1 / (1 + {{ z_2 }} / {{ n }}) *
    (
        {{ p_cc }} +
        {{ z_2 }} / (2 * {{ n }}) -
        {{ z }} / (2 * {{ n }}) *
        SQRT(
            2 *
            {{ n }} *
            {{ p_cc }} *
            (1 - {{ p_cc }}) +
            {{ z_2 }}
        )
    )

{% endmacro %}
