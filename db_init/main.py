import argparse
from urllib.parse import urlparse
from collections import namedtuple
import csv
import os
import logging

from psycopg2 import sql
from omegaconf import OmegaConf
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db_seed import AppConfigSchema
from db_seed.db import ChannelQueue

LOGGER = logging.getLogger()

DbCredentials = namedtuple("TemplateInfo", ["username", "password", "database", "hostname", "port"])


def parse_db_url(url: str) -> DbCredentials:
    result = urlparse(url)

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    return DbCredentials(username, password, database, hostname, port)


def drop_tables(session):
    records = session.execute(
        "SELECT tablename FROM pg_tables WHERE schemaname = %s", ("public",)).all()

    for table_name in records:
        session.execute(sql.SQL("DROP TABLE {0} CASCADE").format(sql.Identifier(table_name[0])))


def main(config: AppConfigSchema):

    if not os.path.isfile(config.path_to_init_csv):
        raise ValueError("You need to specify file with init id of channels")

    channel_id_col = config.channel_id_key

    engine = create_engine(config.database.db_url)

    Session = sessionmaker(bind=engine)

    inserted = 0
    batch_size = 10

    with Session() as session:
        if config.database.drop_tables:
            LOGGER.info("Drop tables")
            drop_tables(session)
            session.commit()

        with open(config.sql_ddl_path, "r", encoding="utf-8") as file:
            LOGGER.info("Init DDL")
            session.execute(file.read())
            session.commit()

        with open(config.path_to_init_csv, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            _ = reader.fieldnames

            for line in reader:
                channel_link = line[channel_id_col]
                channel_link = channel_link.replace("@", "")

                if session.query(ChannelQueue).filter(ChannelQueue.channel_link == channel_link).first() is None:
                    LOGGER.debug("Add channel_id %d to insert batch", channel_link)
                    session.add(ChannelQueue(channel_link=channel_link, status="to_process"))
                    inserted += 1
                    if inserted % batch_size == 0:
                        LOGGER.debug("Add channel_id %d to insert batch", channel_link)
                        session.commit()
                else:
                    LOGGER.debug("Channel id %d already exist skip it", channel_link)

            session.commit()

        LOGGER.info("Insert %d records", inserted)


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
