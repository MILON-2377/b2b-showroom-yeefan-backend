import app.core.database.models
from app.core.database.base import Base

for table_name in sorted(Base.metadata.tables):
    print(table_name)
