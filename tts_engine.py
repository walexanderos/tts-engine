from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (localhost and your future production domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers
)

# This defines the JSON structure the server expects from n8n
class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    # You can change the voice here. 
    # 'en-US-ChristopherNeural' is a great, natural-sounding male voice.
    # 'en-US-AriaNeural' is a great female voice.
    voice = "en-US-ChristopherNeural"
    
    communicate = edge_tts.Communicate(request.text, voice)
    
    # Create a temporary file to hold the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        
    # Generate and save the audio
    await communicate.save(temp_path)
    
    # Read the file back as raw binary data
    with open(temp_path, "rb") as f:
        audio_data = f.read()
        
    # Clean up the temp file
    os.remove(temp_path)
    
    # Return the raw binary audio to n8n
    return Response(content=audio_data, media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    # Runs the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)