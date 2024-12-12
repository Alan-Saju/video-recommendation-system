# config/settings.py
import os

class Config:
    # API Configuration
    API_BASE_URL = "https://api.socialverseapp.com"
    FLIC_TOKEN = "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
    
    # Recommendation Engine Settings
    RECOMMENDATION_PAGE_SIZE = 10
    
    # Caching Configuration
    CACHE_EXPIRY_MINUTES = 60
    
    # Mood-based Recommendation Weights
    MOOD_WEIGHTS = {
        'happy': 1.2,
        'neutral': 1.0,
        'sad': 0.8,
        'excited': 1.3,
        'relaxed': 0.9
    }

    # Category Popularity Boost
    CATEGORY_POPULARITY_BOOST = {
        'trending': 1.5,
        'new': 1.2,
        'classic': 1.0
    }