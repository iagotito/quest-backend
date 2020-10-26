from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///serverquest/database/data.db', echo = True)

Session = sessionmaker(bind=engine)
session = Session()
