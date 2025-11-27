from contextlib import asynccontextmanager
from app.services.config_service import config_service
from sqlmodel import Session
from app.models.database import engine

@asynccontextmanager
async def lifespan(app):
    
    print("-> Starting EVE AI...")
    # =========== STARTUP ===========
    
    with Session(engine) as session:
        config_service.load_from_db(session)
    
    # Register config service
    app.state.config_service = config_service
    yield

    # =========== SHUTDOWN ===========
    
    print("Shutting down EVE AI...")