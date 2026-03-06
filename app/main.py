from fastapi import FastAPI 
from app.api import upload_routes 

app = FastAPI(title="AI image search")

app.include_router(upload_routes.router )


@app.get('/')
async  def root():
    return {
 "message": "AI Image Search API running"
}