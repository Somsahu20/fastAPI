
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

SQL_STRING = f'postgresql://{setting.db_user}:{setting.password}@{setting.db_host}:{setting.db_port}/{setting.db_name}'

#todo : engine manages the connection to the database
engine = create_engine(SQL_STRING, echo=True) 
sessionLocal = sessionmaker(autoflush=False, bind=engine) #todo autommint depreated in sqlalchemy 2.0
# Base = declarative_base() #todo db models inherit from this base superclass. It provides methods and structure to custom made db models