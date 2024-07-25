import pandas as pd

from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException
from textwrap import dedent

def get_account(session: Session) -> str:
    return session.sql('select current_account()').collect()[0][0].lower()

def get_objects(session: Session,
                obj_type: str) -> pd.DataFrame:
    objs = pd.DataFrame(session.sql(f'show {obj_type}').collect())
    objs_records = objs.to_dict(orient='records')
    return objs_records

def get_object_ddl(session: Session,
                   obj_type_singular: str,
                   fully_qualified_obj_name: str) -> str:
    try:
        ddl = session.sql(f"select get_ddl('{obj_type_singular}', '{fully_qualified_obj_name}');").collect()[0][0]
    except SnowparkSQLException as e:
        ddl = dedent(f'''
        /*
            DDL for {fully_qualified_obj_name} is not available
            {e}
        */
        ''')
    return ddl
