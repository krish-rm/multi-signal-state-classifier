"""
Data loading and generation utilities for multi-signal classification.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SignalDataGenerator:
    """Generate synthetic trading and plant health signals for demonstration."""
    
    STATES = ['calm', 'alert', 'risk', 'flow', 'deviation']
    
    def __init__(self, seed: int = 42):
        """Initialize data generator with optional seed for reproducibility."""
        np.random.seed(seed)
        self.seed = seed
    
    def generate_trading_signals(
        self,
        n_samples: int = 1000,
        state_distribution: Optional[dict] = None
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Generate synthetic trading signals.
        
        Args:
            n_samples: Number of samples to generate
            state_distribution: Distribution of states (defaults to even distribution)
        
        Returns:
            Tuple of (signals DataFrame, state labels array)
        """
        if state_distribution is None:
            state_distribution = {state: n_samples // len(self.STATES) 
                                 for state in self.STATES}
        
        signals = []
        labels = []
        
        for state, count in state_distribution.items():
            for _ in range(count):
                if state == 'calm':
                    # Low volatility, stable
                    price_change = np.random.normal(0.001, 0.005)
                    volatility = np.random.normal(0.08, 0.02)
                    volume = np.random.normal(1000000, 100000)
                    rsi = np.random.normal(50, 5)
                    
                elif state == 'alert':
                    # Moderate volatility, some movement
                    price_change = np.random.normal(-0.01, 0.02)
                    volatility = np.random.normal(0.18, 0.03)
                    volume = np.random.normal(1500000, 200000)
                    rsi = np.random.normal(45, 8)
                    
                elif state == 'risk':
                    # High volatility, negative movement
                    price_change = np.random.normal(-0.05, 0.03)
                    volatility = np.random.normal(0.35, 0.05)
                    volume = np.random.normal(2500000, 500000)
                    rsi = np.random.normal(35, 10)
                    
                elif state == 'flow':
                    # Low volatility, positive trend
                    price_change = np.random.normal(0.03, 0.01)
                    volatility = np.random.normal(0.10, 0.02)
                    volume = np.random.normal(900000, 100000)
                    rsi = np.random.normal(60, 5)
                    
                else:  # deviation
                    # Erratic patterns
                    price_change = np.random.normal(0.0, 0.08)
                    volatility = np.random.normal(0.25, 0.10)
                    volume = np.random.normal(2000000, 800000)
                    rsi = np.random.uniform(20, 80)
                
                signals.append({
                    'price_change': price_change,
                    'volatility': volatility,
                    'volume': volume,
                    'rsi': np.clip(rsi, 0, 100)
                })
                labels.append(state)
        
        df = pd.DataFrame(signals)
        return df, np.array(labels)
    
    def generate_plant_health_signals(
        self,
        n_samples: int = 1000,
        state_distribution: Optional[dict] = None
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Generate synthetic plant health signals.
        
        Args:
            n_samples: Number of samples to generate
            state_distribution: Distribution of states
        
        Returns:
            Tuple of (signals DataFrame, state labels array)
        """
        if state_distribution is None:
            state_distribution = {state: n_samples // len(self.STATES) 
                                 for state in self.STATES}
        
        signals = []
        labels = []
        
        for state, count in state_distribution.items():
            for _ in range(count):
                if state == 'calm':
                    # Good conditions, stable
                    soil_moisture = np.random.normal(0.60, 0.05)
                    temperature = np.random.normal(21, 1)
                    stress_score = np.random.normal(0.25, 0.05)
                    
                elif state == 'alert':
                    # Moderate stress, needs attention
                    soil_moisture = np.random.normal(0.45, 0.08)
                    temperature = np.random.normal(24, 2)
                    stress_score = np.random.normal(0.40, 0.08)
                    
                elif state == 'risk':
                    # High stress, urgent
                    soil_moisture = np.random.normal(0.30, 0.08)
                    temperature = np.random.normal(28, 2)
                    stress_score = np.random.normal(0.75, 0.08)
                    
                elif state == 'flow':
                    # Optimal conditions
                    soil_moisture = np.random.normal(0.65, 0.03)
                    temperature = np.random.normal(22.5, 1)
                    stress_score = np.random.normal(0.15, 0.05)
                    
                else:  # deviation
                    # Anomalous readings
                    soil_moisture = np.random.choice(
                        [np.random.normal(0.20, 0.05), np.random.normal(0.85, 0.05)]
                    )
                    temperature = np.random.uniform(15, 30)
                    stress_score = np.random.uniform(0.0, 1.0)
                
                signals.append({
                    'soil_moisture': np.clip(soil_moisture, 0, 1),
                    'temperature': temperature,
                    'stress_score': np.clip(stress_score, 0, 1)
                })
                labels.append(state)
        
        df = pd.DataFrame(signals)
        return df, np.array(labels)
    
    def create_unified_dataset(
        self,
        n_samples: int = 1000,
        state_distribution: Optional[dict] = None
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Create a unified dataset combining trading and plant health signals.
        
        Timeline: Data is collected HOURLY (1 sample per hour)
        - Trading: Hourly intraday snapshots (price_change, volatility, volume, rsi)
        - Plant Health: Hourly IoT sensor readings (soil_moisture, temperature, stress_score)
        - 2,500 samples = ~104 days (~3.5 months) of hourly data
        
        Why Hourly?
        - Enables real-time ambient lighting updates throughout the day
        - Realistic for both use cases (intraday trading, IoT sensors)
        - Provides meaningful state changes that lighting can respond to
        - Allows lighting to reflect current conditions, not just daily summaries
        
        Classification Scope: Point-in-time state classification
        - Each sample represents the state at a specific hour
        - Rolling windows provide historical context (3, 5, 10, 20 hours)
        - Lighting updates hourly based on current state classification
        
        Args:
            n_samples: Number of samples (hours)
            state_distribution: Distribution of states
        
        Returns:
            Tuple of (unified DataFrame, state labels)
        """
        if state_distribution is None:
            state_distribution = {state: n_samples // len(self.STATES) 
                                 for state in self.STATES}
        
        trading_df, trading_labels = self.generate_trading_signals(
            n_samples, state_distribution
        )
        plant_df, plant_labels = self.generate_plant_health_signals(
            n_samples, state_distribution
        )
        
        # Combine signals
        unified_df = pd.concat([trading_df, plant_df], axis=1)
        
        # Add timestamp (hourly collection - enables real-time ambient lighting updates)
        # Hourly is realistic for both: intraday trading snapshots and IoT sensor readings
        start_date = datetime(2023, 1, 1)
        timestamps = [start_date + timedelta(hours=i) for i in range(len(unified_df))]
        unified_df.insert(0, 'timestamp', timestamps)
        
        logger.info(f"Created unified dataset with {len(unified_df)} samples")
        
        return unified_df, trading_labels


def load_or_generate_data(
    output_path: str = "data/processed/unified_signals.parquet",
    n_samples: int = 2500,
    force_generate: bool = False
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Load existing data or generate synthetic data if not available.
    
    Args:
        output_path: Path to save/load data
        n_samples: Number of samples if generating
        force_generate: Force regeneration even if file exists
    
    Returns:
        Tuple of (data DataFrame, labels array)
    """
    import os
    
    if os.path.exists(output_path) and not force_generate:
        logger.info(f"Loading existing data from {output_path}")
        df = pd.read_parquet(output_path)
        # Assuming labels are in a separate column
        if 'state' in df.columns:
            labels = df['state'].values
            return df, labels
    
    logger.info(f"Generating new data with {n_samples} samples")
    generator = SignalDataGenerator()
    
    # Create balanced distribution
    state_distribution = {state: n_samples // len(generator.STATES) 
                         for state in generator.STATES}
    
    df, labels = generator.create_unified_dataset(
        n_samples, state_distribution
    )
    
    # Add labels to dataframe
    df['state'] = labels
    
    # Save to parquet
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"Data saved to {output_path}")
    
    return df, labels


