from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# db_params = {
#     'dbname': 'football_analysis_database',
#     'user': 'postgres',
#     'password': 'root',
#     'host': 'localhost',
#     'port': '5432'
# }
# db_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
DB_URL = os.getenv('DB_URL')
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
