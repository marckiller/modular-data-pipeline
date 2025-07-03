from app.db.database import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)