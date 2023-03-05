import sqlite3
import logging
import time


### Setup ###

# Logging
debug = True

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)
if debug:
    console_handler.setLevel(logging.DEBUG)
    logger.debug("Debugging has been enabled.")
else:
    console_handler.setLevel(logging.INFO)


# DB Setup
conn = sqlite3.connect("testdb.db")
cur = conn.cursor()
tables = {
        "customers": "customer_id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL",
        "products": "product_id INTEGER PRIMARY KEY, title VARCHAR(255) NOT NULL, price FLOAT NOT NULL",
        "orders": "order_seq INT PRIMARY KEY, product INT NOT NULL, quantity INT NOT NULL, owner INT NOT NULL" # where product = product_id and owner = customer_id
    }


### Functions ###

def db_init(conn, cur):
# Check if there already are tables, if not make them:
    try:
        if cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchone() == None:
            for table, columns in tables.items():
                cur.execute(f"CREATE TABLE {table} ({columns});")
                conn.commit()
                logger.info(f"Created table {table}.")
        else:
            logger.error("Table generation is being skipped as they already exist.")
    except:
        logger.ERROR("An unknown error has occured, couldn't generate tables.")
       
        
def list_columns(table: str):
    # List the columns in a table
    columns = []
    logger.debug(f"Searching for column names.")
    for column_name in cur.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}');").fetchall():
        columns.append(str(column_name[0]))
        logger.debug(f"Found column called {column_name[0]}.")
    return (", ".join(columns))
    
    

def select(row: str, table: str):
    # SQL Select function
    return cur.execute(f"SELECT {row} FROM {table};").fetchall()


def insert(table: str, values: tuple):
    parsed_values = "',\n".join("'" + value + "'" for value in values)
    cur.execute(f"""
        INSERT INTO {table} ({list_columns(table)}) VALUES (
        {parsed_values}
        )""")


# def delete():


### Main ###
 
db_init(conn, cur)