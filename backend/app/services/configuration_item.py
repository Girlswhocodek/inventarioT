from sqlalchemy.orm import Session
from sqlalchemy import select
from models.configuration_item import ConfigurationItemDB
from schemas.configuration_item import ConfigurationItemCreate

def get_configuration_items(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(
        select(ConfigurationItemDB)
        .offset(skip)
        .limit(limit)
    ).scalars().all()

def get_configuration_item(db: Session, item_id: int):
    return db.execute(
        select(ConfigurationItemDB)
        .where(ConfigurationItemDB.id == item_id)
    ).scalar_one_or_none()

def create_configuration_item(db: Session, item: ConfigurationItemCreate):
    db_item = ConfigurationItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
