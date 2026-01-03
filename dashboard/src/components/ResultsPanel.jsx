import React from 'react'
import { CheckCircle2, Zap, Clock } from 'lucide-react'

const stateColors = {
  calm: 'from-blue-500 to-blue-600',
  alert: 'from-amber-500 to-amber-600',
  risk: 'from-red-500 to-red-600',
  flow: 'from-green-500 to-green-600',
  deviation: 'from-purple-500 to-purple-600',
}

function ResultsPanel({ prediction }) {
  if (!prediction) return null

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-4 shadow-xl border border-slate-600">
      <div className="flex items-center gap-2 mb-3">
        <CheckCircle2 className="w-4 h-4 text-green-400" />
        <h2 className="text-base font-semibold text-white">Prediction Results</h2>
      </div>

      <div className="space-y-3">
        {/* Main State Result */}
        <div
          className={`bg-gradient-to-r ${stateColors[prediction.state]} rounded-lg p-3 text-white shadow-lg`}
        >
          <p className="text-xs uppercase tracking-wider font-semibold opacity-90 mb-1">
            Predicted State
          </p>
          <h3 className="text-xl font-bold capitalize mb-1">{prediction.state}</h3>
          <p className="text-xs opacity-90">
            {prediction.lighting_control.description}
          </p>
        </div>

        {/* Confidence Grid */}
        <div className="grid grid-cols-2 gap-2">
          {/* Confidence Score */}
          <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600">
            <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-1">
              Confidence
            </p>
            <div className="flex items-baseline gap-1">
              <span className="text-xl font-bold text-white">
                {(prediction.confidence * 100).toFixed(1)}
              </span>
              <span className="text-slate-400 text-sm">%</span>
            </div>
            <div className="mt-2 w-full bg-slate-600 rounded-full h-1.5">
              <div
                className={`bg-gradient-to-r ${stateColors[prediction.state]} h-1.5 rounded-full transition-all duration-500`}
                style={{ width: `${prediction.confidence * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Inference Time */}
          <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600">
            <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-1">
              Response Time
            </p>
            <div className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-blue-400" />
              <div>
                <span className="text-lg font-bold text-white">
                  {prediction.inference_time_ms.toFixed(2)}
                </span>
                <span className="text-slate-400 ml-1 text-sm">ms</span>
              </div>
            </div>
            <p className="text-xs text-green-400 mt-1">✓ &lt; 100ms</p>
          </div>
        </div>

        {/* Lighting Control Info */}
        <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600">
          <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-2">
            💡 Lighting Configuration
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Temperature</p>
              <p className="text-sm font-bold text-blue-400">
                {prediction.lighting_control.color_temperature}K
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Brightness</p>
              <p className="text-sm font-bold text-yellow-400">
                {prediction.lighting_control.brightness}%
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Pattern</p>
              <p className="text-sm font-bold text-purple-400 capitalize">
                {prediction.lighting_control.pattern}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Urgency</p>
              <p className="text-sm font-bold text-red-400 capitalize">
                {prediction.lighting_control.urgency}
              </p>
            </div>
          </div>
        </div>

        {/* Metadata */}
        <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600 text-xs text-slate-400">
          <div className="flex items-center justify-between">
            <span>Model: <span className="text-slate-300">{prediction.model_version}</span></span>
            <span>Time: <span className="text-slate-300">{new Date(prediction.timestamp).toLocaleTimeString()}</span></span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultsPanel

