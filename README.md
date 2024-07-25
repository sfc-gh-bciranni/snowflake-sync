# snowflake-sync

🚧 **Work in Progress - Not for Production Use** 🚧

---

Sync Snowflake object DDLs and Metadata to a local file directory as a starting point for a CI/CD integration.

Pulls DDL and Metadata from `show` command for:

- TABLES
- VIEWS
- STAGES
- FUNCTIONS
- PROCEDURES

Stores in a folder structure.

Usage:

Currently only supported to
- Provide Connection via Snowflake Connections `.toml` file.

```bash
python fetch_snowflake_objects.py --connection my_connection
```

Which creates an account directory as such:

```bash
tree accounts/
```

```
accounts/
└── my_account
    └── databases
        ├── my_first_database
        │   ├── metadata
        │   │   └── my_first_database.yaml
        │   └── schemas
        │       └── public
        │           ├── functions
        │           ├── metadata
        │           │   └── public.yaml
        │           ├── procedures
        │           ├── stages
        │           ├── tables
        │           │   ├── my_first_table.sql
        │           │   └── metadata
        │           │       └── my_first_table.yaml
        │           └── views
        └── my_second_database
            ├── metadata
            │   └── my_second_database.yaml
            └── schemas
                ├── my_first_schema
                │   ├── functions
                │   ├── metadata
                │   │   └── my_first_schema.yaml
                │   ├── procedures
                │   ├── stages
                │   ├── tables
                │   │   ├── my_first_table.sql
                │   │   ├── my_second_table.sql
                │   │   ├── my_third_table.sql
                │   │   ├── my_fourth_table.sql
                │   │   └── metadata
                │   │       ├── my_first_table.yaml
                │   │       ├── my_second_table.yaml
                │   │       ├── my_third_table.yaml
                │   │       └── my_fourth_table.yaml
                │   └── views
                │       ├── metadata
                │       │   └── my_first_view.yaml
                │       └── my_first_view.sql
                └── public
                    ├── functions
                    ├── metadata
                    │   └── public.yaml
                    ├── procedures
                    ├── stages
                    ├── tables
                    └── views
```