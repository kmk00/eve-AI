from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    
    print("Starting EVE AI...")
    # =========== STARTUP ===========
    
    print("EVE AI started.")
    yield

    # =========== SHUTDOWN ===========
    
    print("Shutting down EVE AI...")