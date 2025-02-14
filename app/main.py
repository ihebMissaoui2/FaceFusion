from fastapi import FastAPI
from routes import faceswap_router, lipsync_router
import uvicorn

app = FastAPI(title="FaceFusion API", docs_url="/docs")

# Include routes
app.include_router(faceswap_router.router)
app.include_router(lipsync_router.router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)

