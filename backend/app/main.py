from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import market, analysis

app = FastAPI(
    title="Next-Gen AI Bloomberg Terminal API",
    description="Multi-Agent Autonomous Investment Intelligence Engine",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router)
app.include_router(analysis.router)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Next-Gen AI Bloomberg Engine",
        "version": "1.0.0",
        "agents": ["CIO", "Fundamental Analyst", "Technical Analyst", "Sentiment & News Analyst", "Risk Manager"]
    }
