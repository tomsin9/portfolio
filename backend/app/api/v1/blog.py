from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.db import get_session
from app.models.blog import Blog

router = APIRouter()

# Create a new Blog Post
@router.post("/", response_model=Blog)
def create_blog(blog_data: Blog, session: Session = Depends(get_session)):
    """
    Receive JSON data and store it in the PostgreSQL
    """
    
    # Store the blog data in the session (temporary storage)
    session.add(blog_data)
    
    # Commit the changes to the database (save to the database)
    session.commit()
    
    # Refresh the blog object from the database (get the id or timestamp of the blog)
    session.refresh(blog_data)
    
    return blog_data


# Read all Blog Posts
@router.get("/", response_model=List[Blog])
def read_blogs(session: Session = Depends(get_session)):
    """
    Read all Blog Posts from the PostgreSQL
    """
    statement = select(Blog)
    results = session.exec(statement)
    
    blogs = results.all()
    return blogs


# Read a specific Blog Post
@router.get("/{blog_id}", response_model=Blog)
def read_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog