from fastapi import FastAPI
from app.api.v1.endpoints import top10, engagement

app = FastAPI(title="Netflix Trending API")

app.include_router(top10.router, prefix="", tags=["Top 10"])
app.include_router(engagement.router, prefix="", tags=["Engagement Timeline"])