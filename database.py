import sqlalchemy
from sqlalchemy import create_engine, text  
import os

my_secret = os.environ['DATABASE_KEY_STRING']
engine = create_engine(
my_secret)
#---checking the connection---
# with engine.connect() as conn:
#     result = conn.execute(text("select * from jobs"))
#     jobs = []
#     for row in result.all():
#         jobs.append(dict(row._mapping))
#     print(jobs)