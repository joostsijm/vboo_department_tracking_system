"""Init"""

import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from app.models import Base, Player, State, Department, DepartmentStat


load_dotenv()

# database
engine = create_engine(os.environ["DATABASE_URI"], client_encoding='utf8')
Session = sessionmaker(bind=engine)

# scheduler
scheduler = BackgroundScheduler(
    daemon=True,
    job_defaults={'misfire_grace_time': 10*60},
)
scheduler.start()

# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

# api
BASE_URL = os.environ["API_URL"]
HEADERS = {
    'Authorization': os.environ["AUTHORIZATION"]
}
