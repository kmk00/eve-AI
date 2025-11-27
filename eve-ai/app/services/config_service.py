from sqlmodel import Session, select
from app.models.schemas import Config
from typing import Optional

class ConfigService:
    """Central service for config."""
    
    def __init__(self):
        self._cache: Optional[Config] = None
    
    def load_from_db(self, session: Session) -> Config:
        """
        Load config from database and cache it.
        
        args:
            session: database session
        
        returns:
            Config
        """
        config = session.exec(select(Config)).first()
        if not config:
            # Pierwsze uruchomienie – stwórz default
            config = Config(
                mode="local",
                model_name="gemma3:latest",
                gpu_layers=60,
                temperature=0.7,
                max_tokens=4096,
                conversation_memory_length=10,
                emotion_confidence_threshold=0.6
            )
            session.add(config)
            session.commit()
            session.refresh(config)
        
        self._cache = config
        return config
    
    def get_runtime_config(self) -> Config:
        """
        Get config from cache.
        
        returns:
            Config
        """
        if self._cache is None:
            raise RuntimeError("Config not loaded. Call load_from_db() first.")
        return self._cache
    
    def update_runtime_config(self, session: Session, **fields) -> Config:
        """
        Update config in database.
        
        args:
            session: database session
            **fields: config fields
        
        returns:
            Config
        """
        if self._cache is None:
            raise RuntimeError("Config not loaded. Call load_from_db() first.")
        
        for key, value in fields.items():
            if hasattr(self._cache, key):
                setattr(self._cache, key, value)
            else:
                raise ValueError(f"Invalid config field: {key}")
        
        session.add(self._cache)
        session.commit()
        session.refresh(self._cache)
        return self._cache
    
    def reload_from_db(self, session: Session) -> Config:
        """
        Reload config from database.
        
        args:
            session: database session
        
        returns:
            Config
        """
        self._cache = None
        return self.load_from_db(session)


config_service = ConfigService()