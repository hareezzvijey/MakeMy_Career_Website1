import sqlalchemy
from sqlalchemy import create_engine, text
import os

DB_STRING = db_string = os.getenv('DATABASE_KEY_STRING')
engine = create_engine(DB_STRING)
print(f"DB_STRING = {DB_STRING}")
#---checking the connection---
# with engine.connect() as conn:
#     result = conn.execute(text("select * from jobs"))
#     jobs = []
#     for row in result.all():
#         jobs.append(dict(row._mapping))
#     print(jobs)