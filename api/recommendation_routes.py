# api/recommendation_routes.py
from fastapi import FastAPI, Query
from services.api_client import APIClient
from services.recommendation_engine import RecommendationEngine
from typing import Optional, List, Dict

app = FastAPI()
api_client = APIClient()
recommendation_engine = RecommendationEngine(api_client)

@app.get("/feed")
async def get_recommendations(
    username: str = Query(..., description="Username for personalized recommendations"),
    category_id: Optional[str] = Query(None, description="Optional category filter"),
    mood: Optional[str] = Query(None, description="User's current mood")
) -> List[Dict]:
    """
    Fetch personalized video recommendations
    
    Endpoints:
    1. /feed?username=your_username&category_id=category_id_user_want_to_see&mood=user_current_mood
    2. /feed?username=your_username&category_id=category_id_user_want_to_see
    3. /feed?username=your_username
    """
    recommendations = recommendation_engine.get_recommendations(
        username=username,
        category_id=category_id,
        mood=mood
    )
    return recommendations