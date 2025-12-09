from fastapi import APIRouter, FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.config import API_VERSION
from app.api import chat, config, emotions, analytics, backup, characters, memory, upload
from fastapi.routing import APIRoute

app = FastAPI(title="EVE AI", version="1.0.0",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# HTTP
app.include_router(analytics.router, prefix=f"/api/{API_VERSION}/analytics", tags=["analytics"])
app.include_router(config.router,   prefix=f"/api/{API_VERSION}/config",   tags=["config"])
# app.include_router(config.router,   prefix=f"/api/{API_VERSION}/config",   tags=["config"])
# app.include_router(chat.router,     prefix=f"/api/{API_VERSION}/chat",     tags=["chat"])
# app.include_router(emotions.router, prefix=f"/api/{API_VERSION}/emotions", tags=["emotions"])
# app.include_router(backup.router,   prefix=f"/api/{API_VERSION}/backup",   tags=["backup"])
# app.include_router(characters.router, prefix=f"/api/{API_VERSION}/characters", tags=["characters"])
# app.include_router(memory.router,   prefix=f"/api/{API_VERSION}/memory",   tags=["memory"])
# app.include_router(upload.router,   prefix=f"/api/{API_VERSION}/upload",   tags=["upload"])
print("\n" + "="*60)
print(f"{'METHOD':<10} {'PATH':<40} {'NAME'}")
print("="*60)

found_config = False
for route in app.routes:
    if isinstance(route, APIRoute):
        # if "config" in route.path:
            found_config = True
            methods = ",".join(route.methods)
            print(f"{methods:<10} {route.path:<40} {route.name}")

print("="*60 + "\n")

if not found_config:
    print("❌ NIE ZNALEZIONO ŻADNYCH ROUTÓW 'CONFIG'!")