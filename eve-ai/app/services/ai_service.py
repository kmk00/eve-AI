from typing import Dict, List
import time
import json
from ollama import ChatResponse, chat
from app.models.schemas import Character, Config
from app.services.config_service import config_service


class AI_Service:
    
    def generate_message(self, message: str) -> ChatResponse:
        cfg: Config = config_service.get_runtime_config()
        response: ChatResponse = chat(model=cfg.model_name, messages=[{"role": "user", "content": message}])
        return response
                
    


    def generate_response(self, messages: List[Dict], character: Character) -> tuple[str, str, float]:
        """
        Generate character response using GPU or OpenAI API
        
        :param messages: List of messages, with role and content
        :type messages: List[Dict[role: str, content: str]]
        :param character: AI character to generate response
        :type character: Character
        :return: (response_text, emotion, generation_time_seconds)
        :rtype: tuple[str,str,float]
        """
        system_prompt = f"""You are {character.name}, {character.description}.
        Personality: {character.personality}
        **IMPORTANT:** Always respond in valid JSON: {{"response": <response>, "emotion":"happy|sad|angry|neutral|talking|pouting|embarrassed"}}
        Be concise, reply in user's language, maintain character consistency        
        """
        
        cfg = config_service.get_runtime_config()
        start_time = time.time()
        
        try:
            # Build messages with system prompt
            system_msg = {"role": "system", "content": system_prompt}
            all_messages = [system_msg] + messages
            raw_content = None
            
            
            if cfg.mode == "local":
                # Ollama local API
                response: ChatResponse = chat(
                    model=cfg.model_name,
                    messages=all_messages,
                    format="json",
                    options={
                        "temperature": cfg.temperature,
                        "max_tokens": cfg.max_tokens,
                        "gpu_layers": cfg.gpu_layers
                    }
                )
                raw_content = response.message.content
                
            
            if cfg.mode == "remote":
                raise NotImplementedError
            
            if raw_content is None:
                raise Exception("Failed to generate response")
            
            result = json.loads(raw_content)
            response_text = result.get("response", "No response provided")
            emotion = result.get("emotion", "neutral")
            
            generation_time = time.time() - start_time
            return response_text, emotion, generation_time
            
        except json.JSONDecodeError:
            # Fallback if LLM returns invalid JSON
            generation_time = time.time() - start_time
            return "I had trouble formatting my response correctly.", "neutral", generation_time
            
        except Exception as e:
            # Handle API errors, network issues, etc.
            generation_time = time.time() - start_time
            return f"Error generating response: {str(e)}", "neutral", generation_time
