# utils/metrics.py
import numpy as np
from typing import List, Dict

class RecommendationMetrics:
    @staticmethod
    def mean_absolute_error(predicted: List[float], actual: List[float]) -> float:
        """
        Calculate Mean Absolute Error for recommendations
        """
        return np.mean(np.abs(np.array(predicted) - np.array(actual)))

    @staticmethod
    def root_mean_square_error(predicted: List[float], actual: List[float]) -> float:
        """
        Calculate Root Mean Square Error for recommendations
        """
        return np.sqrt(np.mean((np.array(predicted) - np.array(actual)) ** 2))

    @staticmethod
    def precision_at_k(recommended: List[Dict], relevant: List[str], k: int = 10) -> float:
        """
        Calculate Precision@K for recommendations
        """
        top_k_recommendations = recommended[:k]
        recommended_ids = [rec['video_id'] for rec in top_k_recommendations]
        
        relevant_retrieved = len(set(recommended_ids) & set(relevant))
        return relevant_retrieved / k

    @staticmethod
    def recall_at_k(recommended: List[Dict], relevant: List[str], k: int = 10) -> float:
        """
        Calculate Recall@K for recommendations
        """
        top_k_recommendations = recommended[:k]
        recommended_ids = [rec['video_id'] for rec in top_k_recommendations]
        
        relevant_retrieved = len(set(recommended_ids) & set(relevant))
        return relevant_retrieved / len(relevant) if relevant else 0.0

    def evaluate_recommendations(
        self, 
        recommendations: List[Dict], 
        user_relevant_videos: List[str]
    ) -> Dict[str, float]:
        """
        Comprehensive recommendation evaluation
        """
        return {
            'precision_at_10': self.precision_at_k(recommendations, user_relevant_videos),
            'recall_at_10': self.recall_at_k(recommendations, user_relevant_videos),
            'mae': self.mean_absolute_error(
                [rec['score'] for rec in recommendations], 
                [1.0] * len(recommendations)  # Placeholder actual scores
            ),
            'rmse': self.root_mean_square_error(
                [rec['score'] for rec in recommendations], 
                [1.0] * len(recommendations)  # Placeholder actual scores
            )
        }