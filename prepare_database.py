import sqlalchemy_utils
from sqlalchemy import *

sqlalchemy_utils.functions.drop_database('sqlite:////tmp/test.db')
sqlalchemy_utils.functions.create_database('sqlite:////tmp/test.db')

engine = create_engine('sqlite:////tmp/test.db')

metadata = MetaData()

user = Table('user', metadata,
    Column('id', String(255), primary_key=True)
)

url = Table('url', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', String(255), ForeignKey("user.id"), nullable=False),
    Column('hits', Integer),
    Column('url', String(255), nullable=False),
    Column('shortUrl', String(255), nullable=False)
)

metadata.create_all(engine)