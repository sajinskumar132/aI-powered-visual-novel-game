from fastapi import HTTPException
import ollama
import json
from pydantic import BaseModel


class ApiRequest(BaseModel):
    prompt: str

class ModelRequest:
    def OllamaModel(self, chat_history):
        try:
            response = ollama.chat(
                model="llama3.2",  # Replace with the correct model name
                messages=chat_history,
                format="json"
            )
            return response
        except ollama.exceptions.ModelNotFoundError:
            raise HTTPException(status_code=500, detail="Model not found. Please ensure the model is installed.")
        except ollama.exceptions.OllamaError as e:
            raise HTTPException(status_code=500, detail=f"Ollama Error: {e}")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Error: The Ollama response was not valid JSON.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")