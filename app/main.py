from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse

from app.core import settings
from app.core.utils import oauth
from app.routers import task_router, auth_router
from app.db.utils import connect_to_mongo, close_mongo_connection

app = FastAPI(title=settings.APP_TITLE)

# GOOGLE
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# MIDDLEWARES
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS
app.include_router(task_router)
app.include_router(auth_router)


@app.get('/')
async def root():
    return HTMLResponse('<body><a href="/auth/google/login">Log In</a></body>')


# EVENTS
@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await connect_to_mongo()
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await close_mongo_connection()
    print("Disconnected from MongoDB")
