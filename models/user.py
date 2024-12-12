# models/user.py
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class User:
    username: str
    user_id: str
    interactions: Dict[str, List[str]] = field(default_factory=dict)
    preferences: Dict[str, float] = field(default_factory=dict)
    mood: str = 'neutral'

    def update_interactions(self, interaction_type: str, item_id: str):
        """
        Update user interactions
        """
        if interaction_type not in self.interactions:
            self.interactions[interaction_type] = []
        
        if item_id not in self.interactions[interaction_type]:
            self.interactions[interaction_type].append(item_id)

    def update_preferences(self, category: str, weight: float):
        """
        Update user category preferences
        """
        self.preferences[category] = weight