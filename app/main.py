from fastapi import FastAPI

from app.routers import admin, auth, profile, project, answers


app = FastAPI(title="Projects for people")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(project.router)
app.include_router(answers.router)
app.include_router(admin.router)


