from datetime import datetime
from task_management_system.models import Logged
from sqlalchemy.orm import Session

def clear_expired_sessions(db: Session):
    now = datetime.now()
    db.query(Logged).filter(Logged.expiresAt < now).delete()
    db.commit()



