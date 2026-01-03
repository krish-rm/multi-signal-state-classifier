import React, { useState, useEffect } from 'react'
import { checkHealth } from '../api/prediction'
import { AlertCircle, CheckCircle2, Play, RotateCcw, Sprout, TrendingUp, Monitor } from 'lucide-react'

function InputForm({ formData, onInputChange, onPredict, onReset, loading }) {
  const [apiHealthy, setApiHealthy] = useState(false)
  const [checkingHealth, setCheckingHealth] = useState(true)

  useEffect(() => {
    const checkApi = async () => {
      try {
        await checkHealth()
        setApiHealthy(true)
      } catch {
        setApiHealthy(false)
      } finally {
        setCheckingHealth(false)
      }
    }

    checkApi()
    const interval = setInterval(checkApi, 5000)

    return () => clearInterval(interval)
  }, [])

  const handleInputChange = (e) => {
    onInputChange(e)
  }

  const handleSelectChange = (e) => {
    const { name, value, dataset } = e.target
    const section = dataset.section
    
    // Create a synthetic event with the numeric value
    const syntheticEvent = {
      target: {
        name,
        value: parseFloat(value),
        dataset: { section }
      }
    }
    onInputChange(syntheticEvent)
  }

  const selectClass =
    'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-sm cursor-pointer'

  // Preset values for dropdowns
  const plantMoistureOptions = [
    { value: 0.15, label: 'Low (15%)' },
    { value: 0.30, label: 'Low-Med (30%)' },
    { value: 0.50, label: 'Medium (50%)' },
    { value: 0.65, label: 'Medium-High (65%)' },
    { value: 0.80, label: 'High (80%)' },
    { value: 0.95, label: 'Very High (95%)' },
  ]

  const plantTemperatureOptions = [
    { value: 15.0, label: 'Cool (15°C)' },
    { value: 20.0, label: 'Mild (20°C)' },
    { value: 22.5, label: 'Optimal (22.5°C)' },
    { value: 25.0, label: 'Warm (25°C)' },
    { value: 30.0, label: 'Hot (30°C)' },
    { value: 35.0, label: 'Very Hot (35°C)' },
  ]

  const plantStressOptions = [
    { value: 0.1, label: 'Low (0.1)' },
    { value: 0.3, label: 'Low-Med (0.3)' },
    { value: 0.5, label: 'Medium (0.5)' },
    { value: 0.7, label: 'High (0.7)' },
    { value: 0.9, label: 'Very High (0.9)' },
  ]

  const tradingPriceChangeOptions = [
    { value: -2.5, label: 'Drop (-2.5%)' },
    { value: -1.0, label: 'Down (-1.0%)' },
    { value: -0.5, label: 'Slight Down (-0.5%)' },
    { value: 0.0, label: 'Stable (0%)' },
    { value: 0.02, label: 'Slight Rise (+0.02%)' },
    { value: 0.5, label: 'Slight Up (+0.5%)' },
    { value: 1.0, label: 'Up (+1.0%)' },
    { value: 2.0, label: 'Rise (+2.0%)' },
  ]

  const tradingVolatilityOptions = [
    { value: 0.05, label: 'Very Low (0.05)' },
    { value: 0.15, label: 'Low (0.15)' },
    { value: 0.30, label: 'Medium (0.30)' },
    { value: 0.50, label: 'High (0.50)' },
    { value: 0.75, label: 'Very High (0.75)' },
    { value: 0.90, label: 'Extreme (0.90)' },
  ]

  const tradingVolumeOptions = [
    { value: 500000, label: 'Low (500K)' },
    { value: 1000000, label: 'Medium (1M)' },
    { value: 2500000, label: 'High (2.5M)' },
    { value: 5000000, label: 'Very High (5M)' },
    { value: 10000000, label: 'Extreme (10M)' },
  ]

  const tradingRSIOptions = [
    { value: 20.0, label: 'Oversold (20)' },
    { value: 35.0, label: 'Low (35)' },
    { value: 50.0, label: 'Neutral (50)' },
    { value: 65.5, label: 'High (65.5)' },
    { value: 75.0, label: 'Overbought (75)' },
    { value: 85.0, label: 'Very High (85)' },
  ]

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-4 shadow-xl border border-slate-600">
      {/* API Health Status */}
      <div className="mb-3 p-2 rounded-lg bg-slate-700/50 border border-slate-600 flex items-center gap-2">
        {checkingHealth ? (
          <>
            <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
            <span className="text-xs text-slate-400">Checking API...</span>
          </>
        ) : apiHealthy ? (
          <>
            <CheckCircle2 className="w-4 h-4 text-green-500" />
            <span className="text-xs text-green-400">API Connected</span>
          </>
        ) : (
          <>
            <AlertCircle className="w-4 h-4 text-red-500" />
            <span className="text-xs text-red-400">API Offline</span>
          </>
        )}
      </div>

      {/* Plant Health Signals - Icon with 3 dropdowns in a line */}
      <div className="mb-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-green-500/20 rounded-lg border border-green-500/30">
            <Sprout className="w-6 h-6 text-green-400" />
          </div>
          <h3 className="text-sm font-semibold text-green-400">Plant Sensors</h3>
        </div>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Soil Moisture</label>
            <select
              name="soil_moisture"
              data-section="plant_health"
              value={formData.plant_health.soil_moisture}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {plantMoistureOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Temperature</label>
            <select
              name="temperature"
              data-section="plant_health"
              value={formData.plant_health.temperature}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {plantTemperatureOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Stress Score</label>
            <select
              name="stress_score"
              data-section="plant_health"
              value={formData.plant_health.stress_score}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {plantStressOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Trading Signals - Icon with 4 dropdowns */}
      <div className="mb-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-blue-500/20 rounded-lg border border-blue-500/30">
            <Monitor className="w-6 h-6 text-blue-400" />
          </div>
          <h3 className="text-sm font-semibold text-blue-400">Trading Terminal</h3>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Price Change</label>
            <select
              name="price_change"
              data-section="trading"
              value={formData.trading.price_change}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {tradingPriceChangeOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Volatility</label>
            <select
              name="volatility"
              data-section="trading"
              value={formData.trading.volatility}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {tradingVolatilityOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Volume</label>
            <select
              name="volume"
              data-section="trading"
              value={formData.trading.volume}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {tradingVolumeOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">RSI</label>
            <select
              name="rsi"
              data-section="trading"
              value={formData.trading.rsi}
              onChange={handleSelectChange}
              className={selectClass}
            >
              {tradingRSIOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Predict Button */}
      <button
        onClick={onPredict}
        disabled={loading || !apiHealthy}
        className="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl hover:shadow-blue-500/20 text-base"
      >
        <Play className="w-5 h-5" />
        {loading ? 'Processing...' : 'Run Prediction'}
      </button>
    </div>
  )
}

export default InputForm

