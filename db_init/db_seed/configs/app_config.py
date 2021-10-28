from dataclasses import dataclass, field
from typing import Any, Optional, List
from omegaconf import MISSING


@dataclass
class DbConfigSchema:
    user: Optional[str] = MISSING
    database: Optional[str] = MISSING
    passw: Optional[str] = MISSING
    host: Optional[str] = MISSING
    port: Optional[int] = MISSING
    db_url: str = MISSING
    drop_tables: bool = False

@ dataclass
class AppConfigSchema:
    database: DbConfigSchema = MISSING
    sql_ddl_path: str = MISSING
