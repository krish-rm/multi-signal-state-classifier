import React, { useState, useCallback } from 'react'
import InputForm from './components/InputForm'
import LightBulbVisualization from './components/LightBulbVisualization'
import ProbabilityChart from './components/ProbabilityChart'
import ResultsPanel from './components/ResultsPanel'
import ErrorAlert from './components/ErrorAlert'
import { predictState } from './api/prediction'
import { Activity, Zap } from 'lucide-react'

function App() {
  const [formData, setFormData] = useState({
    trading: {
      price_change: 0.02,
      volatility: 0.15,
      volume: 1000000,
      rsi: 65.5,
    },
    plant_health: {
      soil_moisture: 0.65,
      temperature: 22.5,
      stress_score: 0.3,
    },
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleInputChange = useCallback((e) => {
    const { name, value, dataset } = e.target
    const section = dataset.section

    setFormData((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [name]: parseFloat(value) || 0,
      },
    }))
  }, [])

  const handlePrediction = useCallback(async () => {
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const result = await predictState(formData)
      setPrediction(result)
    } catch (err) {
      setError(err.message || 'Failed to get prediction. Please ensure the API is running.')
    } finally {
      setLoading(false)
    }
  }, [formData])

  const handleReset = useCallback(() => {
    setFormData({
      trading: {
        price_change: 0.02,
        volatility: 0.15,
        volume: 1000000,
        rsi: 65.5,
      },
      plant_health: {
        soil_moisture: 0.65,
        temperature: 22.5,
        stress_score: 0.3,
      },
    })
    setPrediction(null)
    setError(null)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">
                Multi-Signal State Classifier
              </h1>
              <p className="text-xs text-slate-400">
                Interactive Visualization Dashboard
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Left Column: Input Form */}
          <div className="lg:col-span-1">
            <InputForm
              formData={formData}
              onInputChange={handleInputChange}
              onPredict={handlePrediction}
              onReset={handleReset}
              loading={loading}
            />
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-2 space-y-3">
            {prediction ? (
              <>
                {/* Light Bulb Visualization */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-4 shadow-xl border border-slate-600">
                  <div className="flex items-center gap-2 mb-3">
                    <Activity className="w-4 h-4 text-blue-400" />
                    <h2 className="text-base font-semibold text-white">
                      State Visualization
                    </h2>
                  </div>
                  <LightBulbVisualization state={prediction.state} />
                </div>

                {/* Results Panel */}
                <ResultsPanel prediction={prediction} />

                {/* Probability Chart */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-4 shadow-xl border border-slate-600">
                  <div className="flex items-center gap-2 mb-3">
                    <Activity className="w-4 h-4 text-blue-400" />
                    <h2 className="text-base font-semibold text-white">
                      Probability Distribution
                    </h2>
                  </div>
                  <ProbabilityChart probabilities={prediction.probabilities} />
                </div>
              </>
            ) : (
              <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 shadow-xl border border-slate-600 text-center">
                <div className="text-slate-400 mb-2">
                  <Zap className="w-8 h-8 mx-auto mb-2 opacity-50" />
                </div>
                <h3 className="text-base font-semibold text-slate-300 mb-1">
                  No Prediction Yet
                </h3>
                <p className="text-sm text-slate-500">
                  Adjust the input signals and click "Run Prediction" to see results
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700 bg-slate-900/50 mt-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 text-center text-xs text-slate-500">
          <p>Multi-Signal State Classifier v1.0.0 | API Server: http://localhost:8000</p>
        </div>
      </footer>
    </div>
  )
}

export default App

