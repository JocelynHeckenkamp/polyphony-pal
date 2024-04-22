from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateTable
from .models import db

# Set database configuration need to grab from mysqlworkbench
DATABASE_URI = 'mysql+pymysql://username:password@localhost/dbname'


engine = create_engine(DATABASE_URI, echo=True)

# Generate SQL for all tables in models.py
metadata = MetaData()
metadata.reflect(bind=engine)

with engine.connect() as conn:
    # output schema creation SQL for a new database
    conn.execute('CREATE DATABASE IF NOT EXISTS POLYPHONYPAL;')
    conn.execute('USE POLYPHONYPAL;')

    # Output CreateTable statements for all tables
    for table in metadata.sorted_tables:
        create_table_sql = CreateTable(table).compile(conn).string
        print(create_table_sql)