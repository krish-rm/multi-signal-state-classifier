"""
Feature engineering for multi-signal classification.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging

logger = logging.getLogger(__name__)


class TimeSeriesFeatureExtractor:
    """Extract time-series features from signals."""
    
    def __init__(self, windows: List[int] = None):
        """
        Initialize feature extractor.
        
        Note: With hourly data collection, windows represent hours:
        - 3 = last 3 hours
        - 5 = last 5 hours
        - 10 = last 10 hours
        - 20 = last 20 hours (~1 day)
        
        These rolling windows provide short-term context for state classification,
        enabling the ambient lighting to respond to recent trends, not just current values.
        
        Args:
            windows: List of window sizes for rolling statistics (in samples/hours)
        """
        self.windows = windows if windows else [3, 5, 10, 20]
    
    def extract_rolling_stats(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Extract rolling statistics (mean, std, min, max).
        
        Args:
            df: Input dataframe
            columns: Columns to compute rolling stats on
        
        Returns:
            DataFrame with rolling statistics features
        """
        features = pd.DataFrame(index=df.index)
        
        for col in columns:
            if col not in df.columns:
                continue
            
            for window in self.windows:
                # Rolling mean
                features[f'{col}_rolling_mean_{window}'] = df[col].rolling(
                    window=window, min_periods=1
                ).mean()
                
                # Rolling std
                features[f'{col}_rolling_std_{window}'] = df[col].rolling(
                    window=window, min_periods=1
                ).std().fillna(0)
                
                # Rolling min
                features[f'{col}_rolling_min_{window}'] = df[col].rolling(
                    window=window, min_periods=1
                ).min()
                
                # Rolling max
                features[f'{col}_rolling_max_{window}'] = df[col].rolling(
                    window=window, min_periods=1
                ).max()
        
        return features
    
    def extract_trend_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Extract trend indicators (slope, acceleration, change rate).
        
        Args:
            df: Input dataframe
            columns: Columns to compute trends on
        
        Returns:
            DataFrame with trend features
        """
        features = pd.DataFrame(index=df.index)
        
        for col in columns:
            if col not in df.columns:
                continue
            
            # First derivative (rate of change)
            features[f'{col}_change_1'] = df[col].diff()
            
            # Second derivative (acceleration)
            features[f'{col}_change_2'] = df[col].diff().diff()
            
            # Percentage change
            features[f'{col}_pct_change'] = df[col].pct_change()
        
        return features.fillna(0)
    
    def extract_statistical_features(
        self, df: pd.DataFrame, columns: List[str]
    ) -> pd.DataFrame:
        """
        Extract statistical features (skewness, kurtosis).
        
        Args:
            df: Input dataframe
            columns: Columns to analyze
        
        Returns:
            DataFrame with statistical features
        """
        features = pd.DataFrame(index=df.index)
        
        for col in columns:
            if col not in df.columns:
                continue
            
            for window in self.windows:
                series = df[col].rolling(window=window, min_periods=1)
                features[f'{col}_skew_{window}'] = series.skew().fillna(0)
                features[f'{col}_kurt_{window}'] = series.kurt().fillna(0)
        
        return features


class MultiSourceFeatureFusion:
    """Create multi-source fusion features."""
    
    def __init__(self):
        """Initialize feature fusion."""
        pass
    
    def create_cross_source_features(
        self, trading_df: pd.DataFrame, plant_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create cross-source correlation and interaction features.
        
        Args:
            trading_df: Trading signals
            plant_df: Plant health signals
        
        Returns:
            DataFrame with fusion features
        """
        features = pd.DataFrame(index=trading_df.index)
        
        # Create interaction terms
        trading_cols = trading_df.select_dtypes(include=[np.number]).columns
        plant_cols = plant_df.select_dtypes(include=[np.number]).columns
        
        for tcol in trading_cols:
            for pcol in plant_cols:
                # Simple multiplication interaction
                features[f'{tcol}_x_{pcol}'] = (
                    trading_df[tcol] * plant_df[pcol]
                )
                
                # Ratio interaction
                features[f'{tcol}_{pcol}_ratio'] = (
                    trading_df[tcol] / (plant_df[pcol] + 1e-6)
                )
        
        # Cross-correlation features
        for window in [5, 10, 20]:
            for tcol in trading_cols:
                for pcol in plant_cols:
                    corr = trading_df[tcol].rolling(window).corr(
                        plant_df[pcol]
                    )
                    features[f'{tcol}_{pcol}_corr_{window}'] = corr.fillna(0)
        
        return features
    
    def normalize_features(
        self, df: pd.DataFrame, method: str = 'standard'
    ) -> Tuple[pd.DataFrame, dict]:
        """
        Normalize features across sources.
        
        Args:
            df: Input dataframe
            method: 'standard' or 'minmax'
        
        Returns:
            Tuple of (normalized DataFrame, scaler for later use)
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df_copy = df.copy()
        
        if method == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
        df_copy[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        
        return df_copy, scaler
    
    def create_source_specific_zscore(
        self, df: pd.DataFrame, source_col: str
    ) -> pd.DataFrame:
        """
        Create source-specific z-scores.
        
        Args:
            df: Input dataframe with source column
            source_col: Column indicating data source
        
        Returns:
            DataFrame with z-score features per source
        """
        features = pd.DataFrame(index=df.index)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for source in df[source_col].unique():
            mask = df[source_col] == source
            for col in numeric_cols:
                mean = df.loc[mask, col].mean()
                std = df.loc[mask, col].std()
                features[f'{col}_{source}_zscore'] = (
                    (df[col] - mean) / (std + 1e-6)
                )
        
        return features


class FeaturePipeline:
    """Complete feature engineering pipeline."""
    
    def __init__(self):
        """Initialize feature pipeline."""
        self.ts_extractor = TimeSeriesFeatureExtractor()
        self.fusion = MultiSourceFeatureFusion()
        self.scaler = None
        self.feature_cols = []
    
    def fit_transform(
        self, df: pd.DataFrame, target_col: str = 'state'
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        Fit and transform features.
        
        Args:
            df: Input dataframe (must have trading and plant columns)
            target_col: Target column name
        
        Returns:
            Tuple of (engineered features, feature names)
        """
        # Separate signals
        trading_cols = ['price_change', 'volatility', 'volume', 'rsi']
        plant_cols = ['soil_moisture', 'temperature', 'stress_score']
        
        trading_df = df[[c for c in trading_cols if c in df.columns]].copy()
        plant_df = df[[c for c in plant_cols if c in df.columns]].copy()
        
        # Extract time-series features
        trading_ts_features = self.ts_extractor.extract_rolling_stats(
            trading_df, trading_cols
        )
        trading_trend_features = self.ts_extractor.extract_trend_features(
            trading_df, trading_cols
        )
        trading_stat_features = self.ts_extractor.extract_statistical_features(
            trading_df, trading_cols
        )
        
        plant_ts_features = self.ts_extractor.extract_rolling_stats(
            plant_df, plant_cols
        )
        plant_trend_features = self.ts_extractor.extract_trend_features(
            plant_df, plant_cols
        )
        plant_stat_features = self.ts_extractor.extract_statistical_features(
            plant_df, plant_cols
        )
        
        # Fusion features
        fusion_features = self.fusion.create_cross_source_features(
            trading_df, plant_df
        )
        
        # Combine all features
        all_features = pd.concat([
            df[[c for c in trading_cols if c in df.columns]],
            df[[c for c in plant_cols if c in df.columns]],
            trading_ts_features,
            trading_trend_features,
            trading_stat_features,
            plant_ts_features,
            plant_trend_features,
            plant_stat_features,
            fusion_features
        ], axis=1)
        
        # Drop NaN and Inf values
        all_features = all_features.fillna(0)
        all_features = all_features.replace([np.inf, -np.inf], 0)
        
        # Normalize
        all_features, self.scaler = self.fusion.normalize_features(
            all_features, method='standard'
        )
        
        self.feature_cols = all_features.columns.tolist()
        logger.info(f"Created {len(self.feature_cols)} features")
        
        return all_features, self.feature_cols
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform features using fitted pipeline.
        
        Args:
            df: Input dataframe
        
        Returns:
            Engineered features dataframe
        """
        # Similar to fit_transform but uses fitted scaler
        trading_cols = ['price_change', 'volatility', 'volume', 'rsi']
        plant_cols = ['soil_moisture', 'temperature', 'stress_score']
        
        trading_df = df[[c for c in trading_cols if c in df.columns]].copy()
        plant_df = df[[c for c in plant_cols if c in df.columns]].copy()
        
        # Check if single row (common in prediction scenarios)
        is_single_row = len(df) == 1
        
        # Extract features
        trading_ts_features = self.ts_extractor.extract_rolling_stats(
            trading_df, trading_cols
        )
        trading_trend_features = self.ts_extractor.extract_trend_features(
            trading_df, trading_cols
        )
        trading_stat_features = self.ts_extractor.extract_statistical_features(
            trading_df, trading_cols
        )
        
        plant_ts_features = self.ts_extractor.extract_rolling_stats(
            plant_df, plant_cols
        )
        plant_trend_features = self.ts_extractor.extract_trend_features(
            plant_df, plant_cols
        )
        plant_stat_features = self.ts_extractor.extract_statistical_features(
            plant_df, plant_cols
        )
        
        # For single row predictions, enhance raw values to compensate for missing time-series context
        if is_single_row:
            # Use raw values as rolling means (since rolling mean of 1 value = the value itself)
            # This ensures plant health signals are properly represented in rolling features
            for col in plant_cols:
                if col in plant_df.columns:
                    raw_val = plant_df[col].iloc[0]
                    # Set rolling means to the raw value (they should already be, but ensure it)
                    for window in self.ts_extractor.windows:
                        mean_col = f'{col}_rolling_mean_{window}'
                        if mean_col in plant_ts_features.columns:
                            plant_ts_features.loc[plant_ts_features.index[0], mean_col] = raw_val
                        # Set min and max to raw value too
                        min_col = f'{col}_rolling_min_{window}'
                        max_col = f'{col}_rolling_max_{window}'
                        if min_col in plant_ts_features.columns:
                            plant_ts_features.loc[plant_ts_features.index[0], min_col] = raw_val
                        if max_col in plant_ts_features.columns:
                            plant_ts_features.loc[plant_ts_features.index[0], max_col] = raw_val
            
            # Do the same for trading signals
            for col in trading_cols:
                if col in trading_df.columns:
                    raw_val = trading_df[col].iloc[0]
                    for window in self.ts_extractor.windows:
                        mean_col = f'{col}_rolling_mean_{window}'
                        if mean_col in trading_ts_features.columns:
                            trading_ts_features.loc[trading_ts_features.index[0], mean_col] = raw_val
                        min_col = f'{col}_rolling_min_{window}'
                        max_col = f'{col}_rolling_max_{window}'
                        if min_col in trading_ts_features.columns:
                            trading_ts_features.loc[trading_ts_features.index[0], min_col] = raw_val
                        if max_col in trading_ts_features.columns:
                            trading_ts_features.loc[trading_ts_features.index[0], max_col] = raw_val
        
        # Fusion features
        fusion_features = self.fusion.create_cross_source_features(
            trading_df, plant_df
        )
        
        # Combine
        all_features = pd.concat([
            df[[c for c in trading_cols if c in df.columns]],
            df[[c for c in plant_cols if c in df.columns]],
            trading_ts_features,
            trading_trend_features,
            trading_stat_features,
            plant_ts_features,
            plant_trend_features,
            plant_stat_features,
            fusion_features
        ], axis=1)
        
        # Handle missing values
        all_features = all_features.fillna(0)
        all_features = all_features.replace([np.inf, -np.inf], 0)
        
        # Select only fitted features and normalize
        all_features = all_features[[col for col in self.feature_cols 
                                     if col in all_features.columns]]
        
        # Normalize using fitted scaler
        if self.scaler:
            numeric_cols = all_features.select_dtypes(include=[np.number]).columns
            all_features[numeric_cols] = self.scaler.transform(
                all_features[numeric_cols]
            )
        
        return all_features


