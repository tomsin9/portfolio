from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.db import get_session
from app.core.auth import get_current_username
from app.models.blog import Blog

router = APIRouter()

# Create a new Blog Post
@router.post("/", response_model=Blog)
def create_blog(
        blog_input: Blog, 
        session: Session = Depends(get_session), 
        username: str = Depends(get_current_username)
    ):
    """
    Receive JSON data and store it in the PostgreSQL
    """
    
    # Create a new blog object, ensure id is created from database
    db_blog = Blog.model_validate(blog_input)
    
    # Store the blog data in the session (temporary storage)
    session.add(db_blog)
    
    # Commit the changes to the database (save to the database)
    session.commit()
    
    # Refresh the blog object from the database (get the id or timestamp of the blog)
    session.refresh(db_blog)
    
    return db_blog


# Read all Blog Posts
@router.get("/", response_model=List[Blog])
def read_blogs(session: Session = Depends(get_session)):
    """
    Read all Blog Posts from the PostgreSQL
    """
    statement = select(Blog).where(Blog.is_published == True)
    results = session.exec(statement)
    
    blogs = results.all()
    return blogs


# Read a specific Blog Post
@router.get("/{blog_id}", response_model=Blog)
def read_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog or not blog.is_published:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog