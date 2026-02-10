from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import List, Dict, Any

from app.db.session import get_session
from app.core.auth import get_current_username
from app.models.blog import Blog

router = APIRouter()

# Create a new Blog Post
@router.post("/", response_model=Blog)
def create_post(
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
@router.get("/", response_model=Dict[str, Any])
def read_posts(
    *,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),      # Which page, default 1
    size: int = Query(12, ge=1, le=100) # How many records per page, default 12
):
    # 1. Calculate OFFSET (skip how many records)
    # For example, page=2, size=6, offset = (2-1)*6 = 6
    offset = (page - 1) * size

    # 2. Query the data for the current page
    statement = select(Blog).order_by(Blog.date.desc()).offset(offset).limit(size)
    results = session.exec(statement).all()

    # 3. Query the total number (used for Pagination UI)
    total_statement = select(func.count()).select_from(Blog)
    total = session.exec(total_statement).one()

    return {
        "items": results,
        "total": total,
        "page": page,
        "size": size
    }


# Read a specific Blog Post
@router.get("/{blog_id}", response_model=Blog)
def read_post(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog or not blog.is_published:
        raise HTTPException(status_code=404, detail="Post not found")
    return blog


@router.patch("/{blog_id}", response_model=Blog)
def update_post(
    blog_id: int,
    blog_in: Blog,
    session: Session = Depends(get_session),
    username: str = Depends(get_current_username),
):
    db_blog = session.get(Blog, blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Exclude id from being updated, update the rest of the fields dynamically
    blog_data = blog_in.model_dump(exclude_unset=True)
    for key, value in blog_data.items():
        if key != "id":
            setattr(db_blog, key, value)
            
    session.add(db_blog)
    session.commit()
    session.refresh(db_blog)
    return db_blog


@router.delete("/{blog_id}")
def delete_post(
    blog_id: int,
    session: Session = Depends(get_session),
    username: str = Depends(get_current_username),
):
    db_blog = session.get(Blog, blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Post not found")
    
    session.delete(db_blog)
    session.commit()
    return {"ok": True}