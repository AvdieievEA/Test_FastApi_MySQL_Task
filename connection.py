from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:root@localhost/test_api_db')
Session = sessionmaker(bind=engine)
session = Session()

