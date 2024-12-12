# services/api_client.py
import requests
from typing import Dict, List, Optional
from config.settings import Config
import logging
from functools import lru_cache

class APIClient:
    def __init__(self, token: str = Config.FLIC_TOKEN):
        self.token = token
        self.base_url = Config.API_BASE_URL
        self.headers = {
            'Flic-Token': self.token,
            'Content-Type': 'application/json'
        }
    
    @lru_cache(maxsize=100)
    def fetch_paginated_data(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """
        Fetch paginated data from the specified endpoint
        Uses caching to prevent redundant API calls
        """
        if params is None:
            params = {}
        
        params.update({
            'page': params.get('page', 1),
            'page_size': params.get('page_size', 1000)
        })
        
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}", 
                headers=self.headers, 
                params=params
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.RequestException as e:
            logging.error(f"API Request Error: {e}")
            return []
    
    def get_user_interactions(self, username: str) -> Dict:
        """
        Aggregate user interactions across different types
        """
        interactions = {
            'views': self.fetch_paginated_data(f'posts/view', {'username': username}),
            'likes': self.fetch_paginated_data(f'posts/like', {'username': username}),
            'inspired': self.fetch_paginated_data(f'posts/inspire', {'username': username}),
            'ratings': self.fetch_paginated_data(f'posts/rating', {'username': username})
        }
        return interactions