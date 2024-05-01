# Using dbt Python models to utilize Large Language Models

This is a [dbt project](https://docs.getdbt.com/docs/build/projects) that shows how to use OpenAI API in a dbt environment. Specifically, to convert your database text columns into categories, sentiments, and more.

This example uses Snowflake, but it can apply to other databases, some adjustments will be required, though.

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
2.1 Download Shiny packages metadata from [here](https://github.com/rfordatascience/tidytuesday/blob/master/data/2024/2024-04-16/package_details.csv), details on the dataset are [here](https://github.com/rfordatascience/tidytuesday/blob/master/data/2024/2024-04-16/readme.md)
- Alternatively, you can use a lightweight version from this repository [here](https://github.com/Klimmy/analytics-engineer-posts/blob/main/chat_gpt_classification/data/package_details_10_rows.csv)

2.2 Upload to your database. Note, this project uses Snowflake, if you have another database, some adjustments will be required

2.3 Set up `profiles.yml` (see instructions [here](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml))

2.4 Update `source.yml` file to match your database and schema names

### 3. Get the OpenAI API key
Follow quickstart instructions from [official docs](https://platform.openai.com/docs/quickstart)


### 4. Set up Snowflake passwords
If you are using Snowflake, you need to set up `External Access Integration` and store the OpenAI key there. Follow [official instructions](https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration)


### 5. Run dbt
```bash
dbt run
```

This will take Shiny package titles, and create a `package_category` table in your database with category field generated from OpenAI API
==Note, OpenAI API will charge for requests==
