import os
import openai
import pandas as pd
import logging
from snowflake.snowpark.functions import col, lit

SYSTEM_PROMPT = '''You will be provided a list of CRAN R package titles in ``` brackets.
Come up with a category for each title.
Return only categroy names separated by "|" sign.
'''
COL_TO_CATEGORIZE = 'title'
BATCH_SIZE = 5

def model(dbt, session):
    import _snowflake

    dbt.config(
        materialized='incremental',
        incremental_strategy='append',
        full_refresh = False,
        packages=['pandas', 'openai'],
        secrets={'openai_key': 'openai_key', 'openai_org': 'openai_org'},
        external_access_integrations=['openai_external_access_integration'],
        )

    client = openai.OpenAI(
        api_key=_snowflake.get_generic_secret_string('openai_key'),
        organization=_snowflake.get_generic_secret_string('openai_org'),
        )

    df = dbt.ref('package').to_pandas()
    df.drop_duplicates(subset=[COL_TO_CATEGORIZE], inplace=True)
    if dbt.is_incremental:
        categorized_query = f'''
        SELECT DISTINCT "{ COL_TO_CATEGORIZE }" AS primary_key FROM { dbt.this }
        WHERE "category" IS NOT NULL
        '''
        categorized = [row.PRIMARY_KEY for row in session.sql(categorized_query).collect()]
        df = df.loc[~df[COL_TO_CATEGORIZE].isin(categorized), :]
    n_rows = df.shape[0]

    categories = [None for idx in range(n_rows)]
    for idx in range(0, n_rows, BATCH_SIZE):
        df_sliced = df.iloc[idx:idx+BATCH_SIZE, :]
        user_prompt = f'```{ df_sliced[COL_TO_CATEGORIZE].to_list() }```'

        chat_completion = client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt}
            ],
            model='gpt-3.5-turbo',
            temperature=0,
        )
        gpt_response = chat_completion.choices[0].message.content
        gpt_response = [category.strip() for category in gpt_response.split('|')]
        categories[idx:idx + len(gpt_response)] = gpt_response
    df['category'] = categories
    return df
