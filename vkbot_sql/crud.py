from sqlalchemy.orm import Session

from vkbot_sql import models, schemas
from get_db import get_db


def get_item(db: Session, item_id: int):
    return db.query(models.Items).filter(models.Items.id == item_id).first()


def get_item_by_link(db: Session, link: str):
    return db.query(models.Items).filter(models.Items.link == link).first()


def create_item(db: Session, item: schemas.ItemBase):
    db_item = models.Items(link=item.link, text=item.text)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_answer_by_key(db: Session, answer_key: str):
    return db.query(models.Answers).filter(models.Answers.key == answer_key).first()


def get_answers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Answers).offset(skip).limit(limit).all()


def get_answer(key: str):
    return next(get_db()).query(models.Answers).filter(models.Answers.key == key).first().answer


def search_db(query: str, db: Session):
    results = db.query(models.Items)\
        .with_entities(models.Items.text, models.Items.link)\
        .filter(models.Items.text.ilike(f'%{query}%')).all()
    return results
