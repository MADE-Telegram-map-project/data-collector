import os
import psycopg2
from psycopg2 import sql

# It is example only
if __name__ == "__main__":
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    db_database = os.environ["DB_DATABASE"]

    with psycopg2.connect(dbname=db_database, user=db_user, password=db_pass, host=db_host, port=int(db_port)) as connection:
        with connection.cursor() as cur:
            cur.execute(sql.SQL("SELECT * FROM {0}").format(sql.Identifier("ChannelQueue")))
            print("Select query: ", cur.fetchall())
