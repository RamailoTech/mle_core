import os
import sqlalchemy
from ..base import BaseConnector

class PostgresConnector(BaseConnector):
    def __init__(self, db_user=None, db_password=None, db_host=None, db_port=None, db_name=None):
        self.db_user = db_user or os.environ.get("DATABASE_USER")
        self.db_password = db_password or os.environ.get("DATABASE_PASSWORD")
        self.db_host = db_host or os.environ.get("DATABASE_HOST")
        self.db_port = db_port or os.environ.get("DATABASE_PORT")
        self.db_name = db_name or os.environ.get("DATABASE_NAME")

    def get_connection(self):
        engine = sqlalchemy.create_engine(
            f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        return engine
