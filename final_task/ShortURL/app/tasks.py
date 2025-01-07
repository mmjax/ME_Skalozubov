from datetime import datetime
from sqlalchemy.orm import Session

from app.models import URL


def delete_expired_urls(db: Session):
    db.query(URL).filter(URL.expires_at < datetime.utcnow()).delete()
    db.commit()
