const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Make a prediction request to the API
 * @param {Object} formData - The form data with trading and plant_health signals
 * @returns {Promise<Object>} The prediction response
 * @throws {Error} If the API request fails
 */
export async function predictState(formData) {
  const requestBody = {
    timestamp: new Date().toISOString(),
    signals: {
      trading: {
        price_change: formData.trading.price_change,
        volatility: formData.trading.volatility,
        volume: formData.trading.volume,
        rsi: formData.trading.rsi,
      },
      plant_health: {
        soil_moisture: formData.plant_health.soil_moisture,
        temperature: formData.plant_health.temperature,
        stress_score: formData.plant_health.stress_score,
      },
    },
  }

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.detail || `API Error: ${response.status} ${response.statusText}`
      )
    }

    return await response.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
      throw new Error(
        `Cannot connect to API server. Please ensure it is running at ${API_BASE_URL}`
      )
    }
    throw error
  }
}

/**
 * Check API health
 * @returns {Promise<Object>} Health check response
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
    })

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    throw new Error(`Cannot reach API: ${error.message}`)
  }
}

