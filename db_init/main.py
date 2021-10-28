import argparse
from urllib.parse import urlparse
from collections import namedtuple

import psycopg2
from psycopg2 import sql
from omegaconf import OmegaConf

from db_seed import AppConfigSchema

DbCredentials = namedtuple("TemplateInfo", ["username", "password", "database", "hostname", "port"])

def parse_db_url(url: str) -> DbCredentials:
    result = urlparse(url)

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    return DbCredentials(username, password, database, hostname, port)

def drop_tables(connection):
    with connection.cursor() as cur:
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = %s", ("public",))
        records = cur.fetchall()

        for table_name in records:
            cur.execute(sql.SQL("DROP TABLE {0} CASCADE").format(sql.Identifier(table_name[0])))


def main(config: AppConfigSchema):

    result = parse_db_url(config.database.db_url)

    with psycopg2.connect(database=result.database, user=result.username,
                          password=result.password, host=result.hostname, port=result.port) as conn:

        if config.database.drop_tables:
            with conn.cursor() as cur:
                drop_tables(conn)
                conn.commit()

        with open(config.sql_ddl_path, "r", encoding="utf-8") as file:
            with conn.cursor() as cur:
                cur.execute(file.read())
                conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=True,
                        help="A path to YAML configuration file")

    args, reminder = parser.parse_known_args()
    base_config = OmegaConf.load(args.config)
    cli_config = OmegaConf.from_cli(reminder)

    config = OmegaConf.merge(base_config, cli_config)
    schema = OmegaConf.structured(AppConfigSchema)
    config = OmegaConf.merge(schema, config)
    config: AppConfigSchema = OmegaConf.to_object(config)

    main(config)
