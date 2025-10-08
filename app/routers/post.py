from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func

from app import oauth2
# from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]   #tags help to group the endpoints in the docs
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
  
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # filter is like WHERE in SQL
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # return {"post_detail": post}
    return post



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(new_post: Post): #new_post is of type pydantic model, if we wanna convert pydantic model to dictionary: we can do new_post.dict()
#     return {"new_post":f"title {new_post.title} content {new_post.content} published {new_post.published}"}

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    # new_post=models.Post(title=post.title, content=post.content, published=post.published) #this is how we create a new post object of type models.Post
    #if our model has ex. 100 columns then above way is inefficient, so we can do this instead:
    new_post=models.Post(owner_id=current_user.id, **post.model_dump()) #this will unpack all the values from post and pass it to models.Post
    # new_post=models.Post(**post.dict()) # this was used in pydantic v1, now in v2: .model_dump() is used
    db.add(new_post)
    db.commit() #to save the changes
    db.refresh(new_post) #to get the latest data from database
    # return {"data":new_post}
    return new_post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    # post_query.update(post.dict(), synchronize_session=False) # this was used in pydantic v1, now in v2: .model_dump() is used
    # we could hardcode also but inefficient like: post_query.update({"title": post.title, "content": post.content, "published": post.published}, synchronize_session=False)
    db.commit()
    # return {"data": post_query.first()}
    return post_query.first()
