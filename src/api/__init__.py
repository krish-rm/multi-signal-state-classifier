"""
Lighting control mapping based on state classification.
"""

from typing import Dict, Any


def map_state_to_lighting(state: str, confidence: float = 1.0) -> Dict[str, Any]:
    """
    Map ML state classification to lighting control parameters.
    
    Args:
        state: Predicted state (calm, alert, risk, flow, deviation)
        confidence: Confidence score (0-1)
    
    Returns:
        Dictionary with lighting control parameters
    """
    
    lighting_map = {
        'flow': {
            'color_temperature': 5000,  # Blue-white
            'brightness': 80,
            'pattern': 'steady',
            'description': 'Optimal state - everything aligned',
            'urgency': 'low'
        },
        'calm': {
            'color_temperature': 3000,  # Warm white
            'brightness': 50,
            'pattern': 'steady',
            'description': 'Stable state - no action needed',
            'urgency': 'low'
        },
        'alert': {
            'color_temperature': 4000,  # Bright white
            'brightness': 70,
            'pattern': 'gentle_pulsing',
            'description': 'Attention required',
            'urgency': 'medium'
        },
        'risk': {
            'color_temperature': 2000,  # Red-orange
            'brightness': 85,
            'pattern': 'urgent_pulsing',
            'description': 'Problem detected - action required',
            'urgency': 'high'
        },
        'deviation': {
            'color_temperature': 'variable',  # Multicolor
            'brightness': 'variable',  # 60-90%
            'pattern': 'flashing',
            'description': 'Anomaly detected',
            'urgency': 'high'
        }
    }
    
    # Get default if state not found
    lighting_config = lighting_map.get(state, lighting_map['calm'])
    
    # Adjust brightness based on confidence
    if isinstance(lighting_config['brightness'], int):
        base_brightness = lighting_config['brightness']
        # Higher confidence = steady light, lower confidence = more variation
        lighting_config['brightness_adjustment'] = confidence
    
    return lighting_config


def get_all_state_lighting_configs() -> Dict[str, Dict[str, Any]]:
    """
    Get lighting configuration for all states.
    
    Returns:
        Dictionary mapping states to lighting configs
    """
    states = ['calm', 'alert', 'risk', 'flow', 'deviation']
    configs = {}
    
    for state in states:
        configs[state] = map_state_to_lighting(state)
    
    return configs


def describe_lighting_pattern(state: str, confidence: float = 1.0) -> str:
    """
    Get human-readable description of lighting pattern.
    
    Args:
        state: Predicted state
        confidence: Confidence score
    
    Returns:
        Human-readable description
    """
    config = map_state_to_lighting(state, confidence)
    
    desc = f"{config['description']} "
    
    if isinstance(config['brightness'], int):
        if config['brightness'] < 50:
            desc += "(Dim lighting) "
        elif config['brightness'] < 75:
            desc += "(Medium brightness) "
        else:
            desc += "(Bright lighting) "
    
    pattern = config['pattern']
    if 'pulsing' in pattern:
        desc += "- Light pulsing to grab attention"
    elif 'flashing' in pattern:
        desc += "- Light flashing irregularly"
    else:
        desc += "- Steady, stable lighting"
    
    return desc


