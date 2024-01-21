from fastapi import FastAPI
from .routers import person, document, address, work_experience, relative

app = FastAPI()

app.include_router(person.router)
app.include_router(document.router)
app.include_router(address.router)
app.include_router(work_experience.router)
app.include_router(relative.router)