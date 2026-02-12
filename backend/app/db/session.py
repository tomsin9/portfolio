from sqlmodel import Session, create_engine, SQLModel, select
from app.core.config import settings

from app.models.blog import Blog
from app.models.project import Project

# Create a SQLModel engine from the database URL
engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    # Automatically create tables
    SQLModel.metadata.create_all(engine)
    
    # Check if there is any data, if not, insert one (Seed Data)
    with Session(engine) as session:
        statement = select(Blog)
        result = session.exec(statement).first()
        if not result:
            welcome_post = Blog(
                title="Welcome to My Personal Website!",
                excerpt="This is your first blog post generated automatically.",
                content="""## Hello World

Successfully connected **FastAPI** and **Vue 3**! This is your first blog post.

### What's included

- **Backend**: FastAPI with SQLModel
- **Frontend**: Vue 3 with TypeScript, Tailwind CSS, shadcn/vue, GSAP, etc.
- **Database**: PostgreSQL

### Quick start

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

### Next steps

1. Edit this post in the admin panel
2. Add your own projects and blog posts
3. Customise the theme and content

*Happy coding!*""",
                is_published=True,
                tags=["General", "Tech"]
            )
            session.add(welcome_post)
            session.commit()

    # Check if there is any Project data, if not, insert three (Seed Data)
    with Session(engine) as session:
        statement = select(Project)
        result = session.exec(statement).first()
        if not result:
            seed_projects = [
                Project(
                    title="Personal Website",
                    description="Personal portfolio website built with FastAPI and Vue 3.",
                    category="Web",
                    tags=["FastAPI", "Vue", "TypeScript"],
                    github_url="https://github.com",
                    live_url="https://example.com",
                    order="1",
                ),
                Project(
                    title="AI Chatbot Platform",
                    description="A simple AI chatbot platform with OpenAI API.",
                    category="Web",
                    tags=["Python", "SQLModel", "REST API"],
                    order="2",
                ),
                Project(
                    title="Side Project",
                    description="A simple side project to showcase your skills.",
                    category="Other",
                    tags=["Demo", "Full-stack"],
                    order="3",
                ),
            ]
            for p in seed_projects:
                session.add(p)
            session.commit()