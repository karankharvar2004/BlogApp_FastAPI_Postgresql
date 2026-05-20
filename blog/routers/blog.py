from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET all + POST
@router.get("/blogs/", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    return crud.get_blogs(db)


@router.post("/blogs/", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog)


# GET single + PUT + DELETE
@router.get("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    updated = crud.update_blog(db, blog_id, blog)
    if not updated:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated

@router.patch("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def patch_blog(blog_id: int, blog: schemas.BlogUpdate, db: Session = Depends(get_db)):
    updated = crud.patch_blog(db, blog_id, blog)

    if not updated:
        raise HTTPException(status_code=404, detail="Blog not found")

    return updated


@router.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_blog(db, blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Deleted successfully"}