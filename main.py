# Generate the first line of a novel-style story and an image prompt with relevant details. The image should match the story and remain consistent. After each AI-generated story update, the user will respond, and the next line will be generated based on the reply. The output should be in JSON format: {story_name:"<story_name>" story_line: {Ai: "<AI-generated story>", story_image_prompt: "<77-token max prompt>"}}.
from fastapi import FastAPI,HTTPException
from diffusers import StableDiffusionPipeline
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from models.base_models import ApiRequest, ModelRequest


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_SAVE_DIR = "generated_images"

os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

app.mount("/generated_images", StaticFiles(directory=IMAGE_SAVE_DIR), name="generated_images")


model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.enable_attention_slicing()  # Reduce memory usage
pipe.to("cpu")  # Force CPU usage


chat_history = []
model_instance = ModelRequest()


# Api for generating initial story layout
@app.get("/generate_story")
async def generate_inital_story():
    global chat_history

    chat_history = []

    chat_history.append({
        "role": "user",
        "content": """Generate the opening line of a novel-style story along with an image prompt that visually represents it.  
                    The story and image must remain contextually consistent. The background image should dynamically change based on the story’s setting, while a character image is positioned in the foreground. The image should reflect the player’s input, including locations and situations.  

                    After each AI-generated update, the user will respond, and the next line will be generated based on the reply.  

                    The output must be in JSON format, ensuring all fields are required and non-empty:
                    {
                        "story_name": "<Non-empty story title>",
                        "story_line": {
                            "story_content": "<AI-generated story text>",
                            "story_image_prompt": "<Concise 77-token max image prompt, including background context, foreground character, and player-defined elements>"
                        }
                    }
        """
    })
    

    try:
        response = model_instance.OllamaModel(chat_history)
        chat_history.append({"role":"assistant", "content":  response.message.content})
        return {"story": response.message}
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")


# Api for generating story continuation
@app.post("/generate_story_continuation")
async def generate_continuation_of_story(prompt: ApiRequest):
    global chat_history

    chat_history.append({"role": "user", "content":prompt.prompt})
    try:
        response = model_instance.OllamaModel(chat_history)
        chat_history.append({"role":"assistant", "content":  response.message.content})
        return {"story": response.message}
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")
    

# Api for generating image based on the image prompt
@app.post("/generate_story_image")
async def generate_image(prompt: ApiRequest):
  
    image = pipe(prompt=prompt.prompt).images[0]
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.png"
    file_path = os.path.join(IMAGE_SAVE_DIR, filename)
    
    image.save(file_path, format="PNG")
    
    image_url = f"generated_images/{filename}"

    return {"image_url": image_url}

