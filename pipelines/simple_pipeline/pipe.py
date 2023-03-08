from dataclasses import dataclass
import requests
import pandas as pd
import pandera as pa
from pandera.typing import Index, DataFrame, Series
import sqlite3 as sq
import logging
import json
import hashlib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Table schema validation
class InputSchema(pa.SchemaModel):
    year: Series[int] = pa.Field(gt=2000, coerce=True)
    month: Series[int] = pa.Field(ge=1, le=12, coerce=True)
    day: Series[int] = pa.Field(ge=0, le=365, coerce=True)
    

class OutputSchema(pa.SchemaModel):
    year: Series[int] = pa.Field(gt=2000, coerce=True)
    month: Series[int] = pa.Field(ge=1, le=12, coerce=True)
    day: Series[int] = pa.Field(ge=0, le=365, coerce=True)
 
 # Metadata class   
@dataclass
class DbMetadata():
    title: str = "Custom title for your index page"
    description: str = "Some description text can go here"
    source: str = "Original Data Source"
    source_url: str = "http://example.com/"
    license: str = "ODbL"
    license_url: str = "https://opendatacommons.org/licenses/odbl/"
    source: str = "Original Data Source"
    source_url: str = "http://example.com/"
    hash: str = "md5 hash of the data"
    
    
    

# Task functions

def extract(url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv") -> pd.DataFrame:
    '''
    Extracts data from NY Times github repo
    '''
    
    logger.info("Extracting data from NY Times")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(response.content.decode("utf-8"))
    
    except requests.exceptions.HTTPError as e:
        logger.error(e)
        raise
    
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise
    
    finally:
        logger.info("Finished extracting data from NY Times")

@pa.check_types
def transform(df: DataFrame[InputSchema]) -> DataFrame[OutputSchema]:
    '''
    Transforms the data to a format that is easier to work with
    '''
    df = df.groupby(["date", "state"]).sum().reset_index()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["day"] = df["date"].dt.day
    df = df.drop("date", axis=1)
    return df

def _df_to_sqlite(df: pd.DataFrame, table_name: str) -> None:
    '''
    Writes the data to a sqlite db
    '''
    columns_index = ['year', 'month', 'day']
    index_str = ', '.join([ f'CREATE INDEX idx_{table_name}_{column} ON {table_name} ({column})"' for column in columns_index])
    
    with sq.connect(f'{table_name}.db') as connection:
        df.to_sql(table_name, connection, if_exists='replace', index=False) # writes to sqlite db
        connection.execute(index_str)


def _create_hash(table_name: str) -> str:
    '''
    Creates a hash of the data
    '''
    md5_check = hashlib.md5()

    with open(table_name, "rb") as f:
        for chunk in iter(lambda: f.read(5), b""):
            md5_check.update(chunk)
    
    return md5_check.hexdigest()

        
def _create_metadata_json(table_name: str) -> None:
    '''
    writes the metadata to a json file
    '''
    metadata = DbMetadata(title=f'{table_name} data',
                          
                          source=f'{table_name}.db',
                          description=f'{table_name} data',
                          
                          hash=_create_hash(f'{table_name}.db')
    
    with open(f'{table_name}.json', 'w') as f:
        f.write(json.dumps(metadata.__dict__))

def load(df: pd.DataFrame, table_name: str = 'table_name')-> None:
    '''
    Loads the data into a sqlite db
    '''
    _df_to_sqlite(df, table_name)
    _create_metadata_json(table_name)
    

# Pipeline
def main():
    try:
        df = extract()
        df = transform(df)
        load(df)
    except Exception as e:
        logger.error(e)
        raise
        
if __name__ == "__main__":
    main()
