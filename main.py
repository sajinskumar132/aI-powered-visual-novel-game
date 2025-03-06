# from fastapi import FastAPI

# app=FastAPI()

# @app.get('/hello')
# async def hello():
#     return "Hello"

from fastapi import FastAPI,HTTPException
from diffusers import StableDiffusionPipeline
import torch
import ollama
from io import BytesIO
from fastapi.responses import StreamingResponse
import torch
print("CUDA available:", torch.cuda.is_available())  # Should print False
print("Device:", torch.device("cpu"))  # Should print 'cpu'
app = FastAPI()

# Load the Stable Diffusion model
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe.to("cpu")
chat_history = []
@app.post("/generate_story_prompt/")
async def generate_response(prompt: str):
    global chat_history

    # Append user's input to the chat history
    chat_history.append({"role": "user", "content":prompt})

    # response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt,format:['json']}])
    # return response.message
     # Ensure chat history is formatted correctly
    response = ollama.chat(
        model="llama3.2",
        messages=chat_history,
        format="json"  # Force JSON output
    )

    # Ensure response is valid
    if not response or not response.message:
        raise HTTPException(status_code=500, detail="Failed to generate response")

    # Parse AI response
    ai_message = response.message
    print(response.message.content)
    # Append AI response to chat history
    chat_history.append({"role": "assistant", "content": response.message.content})

    return {"story": ai_message}  # Returning structured output

@app.post("/generate/")
async def generate_image(prompt: str):
    image = pipe(prompt).images[0]

    # Convert image to byte stream
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")

# Run the server: uvicorn filename:app --host 0.0.0.0 --port 8000 --reload
