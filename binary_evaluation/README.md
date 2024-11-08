# Using dbt Python models to utilize Large Language Models

This is a [dbt project](https://docs.getdbt.com/docs/build/projects) that shows how to calculate binary variables average values in robust way.

This example uses BigQuery, but it can apply to other databases, some adjustments will be required, though.

## How to

### 1. Set up environment

Tested with Python 3.12:
```bash
python3 -m venv env/
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Prepare source data
2.1 Connect your BigQuery to the GA4 Public [dataset](https://console.cloud.google.com/marketplace/product/obfuscated-ga360-data/obfuscated-ga360-data). Follow [instructions](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset)
- Alternatively, you can use an aggregated version from this repository [here](https://github.com/Klimmy/analytics-engineer-posts/blob/main/binary_evaluation/data/traffic_sources_aggregated.csv)

2.2 Set up `profiles.yml` (see instructions [here](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml))

2.3 Update `source.yml` file to match your database and schema names

### 3. Run dbt
```bash
dbt run
```

This will take raw web data and calculate conversation rate using several approaches.
