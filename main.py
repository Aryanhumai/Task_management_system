# from fastapi import FastAPI
# from task_management_system.database import Base, engine
# from task_management_system import models

# from task_management_system.routers import auth_routes as dr
# from task_management_system.routers import user_routes as br
# Base.metadata.create_all(bind=engine)
# from task_management_system.routers import task_routes as tr
# from task_management_system.routers import worklog_routes as ur
# from task_management_system.routers import reports_routes as rr


# app = FastAPI(
# title="WELCOME TO MY TASK MANAGEMENT SYSTEM",
# description="by Aryan Bhatia"
# )
# @app.get("/")
# def root():
#     return {"message": "Welcome to the Task Management System"}


# app.include_router(dr.router, prefix="/users", tags=["Login"])
# app.include_router(br.router, tags=["Users"])
# app.include_router(tr.router, tags=["Tasks"])
# app.include_router(ur.router, tags=["Works"])
# app.include_router(rr.router, tags=["Reports"])

# ---

# from fastapi import FastAPI
# from task_management_system.routers import (
#     auth_routes,
#     user_routes,
#     task_routes,
#     worklog_routes,
#     reports_routes,
# )

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Task Management System API"}


# # Include routers
# app.include_router(auth_routes.router, prefix="/auth", tags=["Login"])
# app.include_router(user_routes.router, prefix="/users", tags=["Users"])
# app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
# app.include_router(worklog_routes.router, prefix="/worklogs", tags=["Worklogs"])
# app.include_router(reports_routes.router, prefix="/reports", tags=["Reports"])

# ------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models

# Import routers
from .routers import auth_routes as dr
from .routers import user_routes as br
from .routers import task_routes as tr
from .routers import worklog_routes as ur
from .routers import reports_routes as rr

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title="WELCOME TO MY TASK MANAGEMENT SYSTEM",
    description="by Aryan Bhatia"
)

# ✅ ADD THIS CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/")
def root():
    return {"message": "Welcome to the Task Management System"}

# Register routers
app.include_router(dr.router, prefix="/auth", tags=["Login"])
app.include_router(br.router, prefix="/users", tags=["Users"])
app.include_router(tr.router, prefix="/tasks", tags=["Tasks"])
app.include_router(ur.router, prefix="/worklogs", tags=["Works"])
app.include_router(rr.router, prefix="/reports", tags=["Reports"])


# --------

# from fastapi import FastAPI
# from .database import Base, engine, SessionLocal
# from . import models
# from .utils import hash_password  # make sure this function exists (in utils/__init__.py)

# # Import routers (relative imports)
# from .routers import auth_routes as dr
# from .routers import user_routes as br
# from .routers import task_routes as tr
# from .routers import worklog_routes as ur
# from .routers import reports_routes as rr

# # Create database tables
# Base.metadata.create_all(bind=engine)

# # Initialize FastAPI app
# app = FastAPI(
#     title="WELCOME TO MY TASK MANAGEMENT SYSTEM",
#     description="by Aryan Bhatia"
# )

# # Function to create an initial admin user
# def create_initial_admin():
#     from sqlalchemy.orm import Session
#     db: Session = SessionLocal()
#     admin_email = "admin@example.com"
#     admin_user = db.query(models.User).filter(models.User.email == admin_email).first()

#     if not admin_user:
#         new_admin = models.User(
#             name="admin",
#             email=admin_email,
#             hashed_password=hash_password("admin123"),  # password = admin123
#             is_admin=True
#         )
#         db.add(new_admin)
#         db.commit()
#         print("✅ Admin user created: admin@example.com / admin123")
#     else:
#         print("ℹ️ Admin already exists.")
#     db.close()

# # Create admin when app starts
# create_initial_admin()


# # Root endpoint
# @app.get("/")
# def root():
#     return {"message": "Welcome to the Task Management System"}


# # Register routers (fix prefixes)
# app.include_router(dr.router, prefix="/auth", tags=["Login"])
# app.include_router(br.router, prefix="/users", tags=["Users"])
# app.include_router(tr.router, prefix="/tasks", tags=["Tasks"])
# app.include_router(ur.router, prefix="/worklogs", tags=["Works"])
# app.include_router(rr.router, prefix="/reports", tags=["Reports"])

