from sqlalchemy.orm import Session

from vkparsingapp_sql import models, schemas


def get_items(db: Session):
    return db.query(models.Item)


def create_items(db: Session, item: schemas.ItemBase):
    db_item = models.Item(link=item.link, text=item.text)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_answers(db: Session):
    return db.query(models.Answers)
