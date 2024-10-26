"""Module defines type annotations for use with SQLAlchemy models"""

from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


INT_PK = Annotated[int, mapped_column(primary_key=True, nullable=False)]
CREATED_AT_DATETIME = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    ),
]
