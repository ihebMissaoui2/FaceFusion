import uvicorn
from fastapi import FastAPI

from routes import faceswap, lipsync

app = FastAPI(title="FaceFusion API", docs_url="/docs")

# Include routes
app.include_router(faceswap.router)
app.include_router(lipsync.router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
