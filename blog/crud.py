from sqlalchemy.orm import Session
from . import models, schemas

def get_blogs(db: Session):
    return db.query(models.Blog).all()

def create_blog(db: Session, blog: schemas.BlogCreate):
    db_blog = models.Blog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def update_blog(db: Session, blog_id: int, blog: schemas.BlogCreate):
    db_blog = get_blog(db, blog_id)
    if not db_blog:
        return None

    for key, value in blog.dict().items():
        setattr(db_blog, key, value)

    db.commit()
    db.refresh(db_blog)
    return db_blog

def patch_blog(db: Session, blog_id: int, blog: schemas.BlogUpdate):
    db_blog = get_blog(db, blog_id)
    if not db_blog:
        return None

    update_data = blog.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_blog, key, value)

    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if not db_blog:
        return None

    db.delete(db_blog)
    db.commit()
    return True