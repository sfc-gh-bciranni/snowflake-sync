import argparse
import os

from src import (
    file_manager as fm,
    snowflake_manager as sm,
)

from snowflake.snowpark import Session

CURRENT_DIR = os.getcwd()

object_types = [
    'TABLES',
    'VIEWS',
    'STAGES',
    'FUNCTIONS',
    'PROCEDURES',
]

def main(session: Session) -> None:
    acc = sm.get_account(session)
    acc_dir = fm.make_dir(f'accounts/{acc}', CURRENT_DIR)

    dbs = sm.get_objects(session, 'DATABASES')
    dbs_base_dir = os.path.join(acc_dir, 'databases')
    os.makedirs(dbs_base_dir, exist_ok=True)

    for db in dbs:
        db_name = db['name'].lower()
        if db_name == 'snowflake':
            continue
        db_dir = fm.make_dir(db_name, dbs_base_dir)
        fm.write_object_yaml(db, db_dir)

        schemas = sm.get_objects(session, f'SCHEMAS IN DATABASE {db_name}')
        schemas_base_dir = os.path.join(db_dir, 'schemas')
        os.makedirs(schemas_base_dir, exist_ok=True)

        for schema in schemas:
            schema_name = schema['name'].lower()
            if schema_name == 'information_schema':
                continue
            schema_dir = fm.make_dir(schema_name, schemas_base_dir)
            fm.write_object_yaml(schema, schema_dir)

            for obj_type in object_types:
                objs = sm.get_objects(session, f'{obj_type} IN SCHEMA {db_name}.{schema_name}')
                obj_dir = fm.make_dir(obj_type.lower(), schema_dir)
                for obj in objs:
                    if obj.get('is_builtin') == 'Y':
                        continue
                    obj_name = obj['name'].lower()
                    obj_fqn = f'{db_name}.{schema_name}.{obj_name}'
                    ddl = sm.get_object_ddl(session, obj_type[:-1], obj_fqn)
                    fm.write_object_yaml(obj, obj_dir)
                    fm.write_object_ddl(ddl, obj_name, obj_dir)
    

if __name__ == '__main__':
    # create an argument parser
    parser = argparse.ArgumentParser(description='Fetch Snowflake objects')

    # add required and optional argument groups
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Two ways do connect to Snowflake
    # --> Either supply a connection name, or the connection details

    # 1. Connection name
    optional.add_argument('--connection', '-c', type=str, help='Snowflake connection name', required=False)

    # 2. Connection details
    optional.add_argument('--account', '-a', type=str, help='Snowflake account name', required=False)
    optional.add_argument('--user', '-u', type=str, help='Snowflake user name', required=False)
    optional.add_argument('--password', '-pw', type=str, help='Snowflake password', required=False)
    optional.add_argument('--database', '-db', type=str, help='Snowflake database name', required=False)
    optional.add_argument('--schema', '-s', type=str, help='Snowflake schema name', required=False)
    optional.add_argument('--warehouse','-wh', type=str, help='Snowflake warehouse name', required=False)
    optional.add_argument('--role', '-rl', type=str, help='Snowflake role name', required=False)
    optional.add_argument('--authenticator', '-auth', type=str, help='Snowflake authenticator', required=False)

    # Databases to fetch
    optional.add_argument('--databases', type=str, help='Comma separated list of databases to fetch', required=False)

    # Add the output directory
    optional.add_argument('--output', type=str, help='Output directory', required=False)

    # parse the arguments
    args: argparse.Namespace = parser.parse_args()

    if args.connection:
        print(f'Connection name: {args.connection}')
    
    session = Session.builder.config("connection_name", args.connection).create()

    main(session)

    

