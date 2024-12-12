_# utils/data_preprocessor.py
import numpy as np
import pandas as pd
from typing import List, Dict

class DataPreprocessor:
    def preprocess_user_interactions(self, interactions: List[Dict]) -> pd.DataFrame:
        """
        Preprocess and normalize user interaction data
        """
        df = pd.DataFrame(interactions)
        
        # Handle missing values
        df.fillna(0, inplace=True)
        
        # Normalize engagement features
        engagement_columns = ['views', 'likes', 'ratings']
        df[engagement_columns] = df[engagement_columns].apply(
            lambda x: (x - x.min()) / (x.max() - x.min())
        )
        
        return df
    
    def extract_video_features(self, videos: List[Dict]) -> np.ndarray:
        """
        Extract and vectorize video metadata features
        """
        # Implement feature extraction logic
        pass