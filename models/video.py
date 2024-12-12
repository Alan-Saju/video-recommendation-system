# utils/data_preprocessor.py
import numpy as np
import pandas as pd
from typing import List, Dict, Any
import re
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

class DataPreprocessor:
    def __init__(self):
        # Initialize feature extraction components
        self.tfidf_vectorizer = TfidfVectorizer(max_features=50)
        self.tag_binarizer = MultiLabelBinarizer()
        self.scaler = StandardScaler()

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
        
        Feature extraction includes:
        1. Textual features (title, description)
        2. Categorical features
        3. Numerical features
        4. Tag-based features
        """
        # Prepare feature matrices
        textual_features = self._extract_textual_features(videos)
        numerical_features = self._extract_numerical_features(videos)
        categorical_features = self._extract_categorical_features(videos)
        tag_features = self._extract_tag_features(videos)
        
        # Combine all features
        combined_features = np.hstack([
            textual_features,
            numerical_features,
            categorical_features,
            tag_features
        ])
        
        return combined_features

    def _extract_textual_features(self, videos: List[Dict]) -> np.ndarray:
        """
        Extract TF-IDF features from title and description
        """
        # Combine title and description
        texts = [
            f"{video.get('title', '')} {video.get('description', '')}" 
            for video in videos
        ]
        
        # Fit and transform text features
        return self.tfidf_vectorizer.fit_transform(texts).toarray()

    def _extract_numerical_features(self, videos: List[Dict]) -> np.ndarray:
        """
        Extract and normalize numerical features
        """
        # Define numerical features to extract
        numerical_columns = [
            'views', 'likes', 'duration', 'engagement_score', 
            'creation_timestamp', 'popularity_score'
        ]
        
        # Extract numerical features
        numerical_data = []
        for video in videos:
            row = []
            for col in numerical_columns:
                # Safely extract numerical value, default to 0 if not found
                value = video.get(col, 0)
                row.append(value)
            numerical_data.append(row)
        
        # Convert to numpy array and scale
        numerical_array = np.array(numerical_data)
        return self.scaler.fit_transform(numerical_array)

    def _extract_categorical_features(self, videos: List[Dict]) -> np.ndarray:
        """
        One-hot encode categorical features
        """
        # Define categorical features
        categorical_columns = [
            'category', 'language', 'content_type'
        ]
        
        # One-hot encoding
        categorical_data = []
        for video in videos:
            row = []
            for col in categorical_columns:
                # Get categorical value, default to 'unknown'
                value = video.get(col, 'unknown')
                row.append(value)
            categorical_data.append(row)
        
        # Use pandas get_dummies for one-hot encoding
        categorical_df = pd.DataFrame(categorical_data, columns=categorical_columns)
        return pd.get_dummies(categorical_df).values

    def _extract_tag_features(self, videos: List[Dict]) -> np.ndarray:
        """
        Extract features from video tags
        """
        # Extract tags from videos
        tags = [video.get('tags', []) for video in videos]
        
        # Fit and transform tags using MultiLabelBinarizer
        return self.tag_binarizer.fit_transform(tags)

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text features
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Remove extra whitespaces
        text = ' '.join(text.split())
        
        return text

def create_feature_extractor() -> DataPreprocessor:
    """
    Factory method to create a configured DataPreprocessor
    """
    return DataPreprocessor()