from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.project import Project
from app.schemas.project import ProjectRead

router = APIRouter()

@router.get("/", response_model=List[ProjectRead])
def read_projects(session: Session = Depends(get_session)):
    statement = select(Project).order_by(Project.order, Project.updated_at.desc())
    return session.exec(statement).all()


@router.post("/", response_model=Project)
def create_project(
        *,
        session: Session = Depends(get_session),
        project_in: Project,
        username: str = Depends(get_current_user)
    ):
    # db_project = Project.model_validate(project_in)
    
    session.add(project_in)
    session.commit()
    session.refresh(project_in)
    return project_in


@router.patch("/{project_id}", response_model=Project)
def update_project(
        project_id: int, 
        project_in: Project, 
        session: Session = Depends(get_session),
        username: str = Depends(get_current_user)
    ):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Exclude id from being updated, update the rest of the fields dynamically
    project_data = project_in.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        if key != "id":
            setattr(db_project, key, value)
            
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
def delete_project(
        project_id: int, 
        session: Session = Depends(get_session), 
        username: str = Depends(get_current_user)
    ):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    session.delete(db_project)
    session.commit()
    return {"ok": True}