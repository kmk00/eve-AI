from typing import Dict, List

from ollama import ChatResponse, chat
from app.models.schemas import Character, Config
from app.services.config_service import config_service

class AI_Service:
    
    def generate_message(self, message: str) -> ChatResponse:
        cfg: Config = config_service.get_runtime_config()
        response: ChatResponse = chat(model=cfg.model_name, messages=[{"role": "user", "content": message}])
        print(response.message.content)
        return response
                
    
    # def generate_response(self,messages:List[Dict], character: Character) -> tuple:
    #     raise NotImplementedError