from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    voice = "en-US-ChristopherNeural"
    
    communicate = edge_tts.Communicate(request.text, voice)
    
    # NEW: Create an empty byte string to hold the audio in RAM
    audio_bytes = b""
    
    # NEW: Stream the generation directly into memory
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
            
    # Return the bytes directly to React
    return Response(content=audio_bytes, media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)