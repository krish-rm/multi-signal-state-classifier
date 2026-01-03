import React, { useMemo } from 'react'

const stateConfig = {
  calm: {
    color: '#3B82F6',
    glow: '#3B82F6',
    animation: 'animate-pulse-slow',
    description: 'Stable - No action needed',
    pattern: 'Steady',
  },
  alert: {
    color: '#F59E0B',
    glow: '#F59E0B',
    animation: 'animate-pulse',
    description: 'Attention Required',
    pattern: 'Gentle Pulsing',
  },
  risk: {
    color: '#EF4444',
    glow: '#EF4444',
    animation: 'animate-pulse-fast',
    description: 'Problem Detected',
    pattern: 'Urgent Pulsing',
  },
  flow: {
    color: '#10B981',
    glow: '#10B981',
    animation: 'animate-pulse-slow',
    description: 'Everything Optimal',
    pattern: 'Smooth Steady',
  },
  deviation: {
    color: '#8B5CF6',
    glow: '#8B5CF6',
    animation: 'animate-flash',
    description: 'Anomaly Present',
    pattern: 'Flashing',
  },
}

function LightBulbVisualization({ state = 'calm' }) {
  const config = useMemo(() => stateConfig[state] || stateConfig.calm, [state])

  return (
    <div className="space-y-3">
      {/* Main Light Bulb */}
      <div className="flex flex-col items-center justify-center py-3">
        <div className="relative w-24 h-24">
          {/* Glow effect */}
          <div
            className={`absolute inset-0 rounded-full ${config.animation} blur-3xl opacity-50`}
            style={{ backgroundColor: config.color }}
          ></div>

          {/* Bulb outer circle */}
          <svg className="w-full h-full" viewBox="0 0 200 200">
            <defs>
              <radialGradient id="bulbGradient" cx="35%" cy="35%">
                <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.9" />
                <stop offset="70%" stopColor={config.color} stopOpacity="0.8" />
                <stop offset="100%" stopColor={config.color} stopOpacity="0.4" />
              </radialGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                <feMerge>
                  <feMergeNode in="coloredBlur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Bulb shape */}
            <g filter="url(#glow)">
              {/* Main bulb */}
              <circle
                cx="100"
                cy="90"
                r="70"
                fill="url(#bulbGradient)"
                stroke={config.color}
                strokeWidth="2"
              />

              {/* Bulb highlight */}
              <circle
                cx="75"
                cy="60"
                r="20"
                fill="#FFFFFF"
                opacity="0.6"
              />

              {/* Socket */}
              <rect
                x="85"
                y="155"
                width="30"
                height="15"
                rx="2"
                fill="#333333"
                stroke="#555555"
                strokeWidth="1"
              />

              {/* Base threads */}
              <line x1="92" y1="165" x2="92" y2="172" stroke="#666666" strokeWidth="1" />
              <line x1="100" y1="165" x2="100" y2="172" stroke="#666666" strokeWidth="1" />
              <line x1="108" y1="165" x2="108" y2="172" stroke="#666666" strokeWidth="1" />
            </g>
          </svg>
        </div>

        {/* State Label */}
        <h3 className="mt-2 text-xl font-bold text-white capitalize">
          {state}
        </h3>
        <p className="text-slate-300 text-sm mt-1">
          {config.description}
        </p>
      </div>

      {/* State Info Grid */}
      <div className="grid grid-cols-2 gap-2">
        {/* Pattern */}
        <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600">
          <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-0.5">
            Pattern
          </p>
          <p className="text-sm font-bold text-white">
            {config.pattern}
          </p>
        </div>

        {/* Color */}
        <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600">
          <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-0.5">
            Color
          </p>
          <div className="flex items-center gap-1.5">
            <div
              className="w-4 h-4 rounded-full border border-slate-500"
              style={{ backgroundColor: config.color }}
            ></div>
            <p className="text-sm font-bold text-white">
              {config.color}
            </p>
          </div>
        </div>
      </div>

      {/* State Meanings */}
      <div className="p-2 bg-slate-700/50 rounded-lg border border-slate-600">
        <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-1">
          What This Means
        </p>
        <div className="space-y-1 text-xs text-slate-300">
          {state === 'calm' && (
            <>
              <p>✓ System operating normally</p>
              <p>✓ No immediate action required</p>
              <p>✓ All signals within safe ranges</p>
            </>
          )}
          {state === 'alert' && (
            <>
              <p>⚠ Monitor system closely</p>
              <p>⚠ Some signals trending differently</p>
              <p>⚠ Be prepared to take action if needed</p>
            </>
          )}
          {state === 'risk' && (
            <>
              <p>🚨 Immediate attention needed</p>
              <p>🚨 One or more critical signals detected</p>
              <p>🚨 Consider taking corrective action</p>
            </>
          )}
          {state === 'flow' && (
            <>
              <p>✨ Optimal conditions detected</p>
              <p>✨ All systems performing excellently</p>
              <p>✨ Perfect alignment across signals</p>
            </>
          )}
          {state === 'deviation' && (
            <>
              <p>⚡ Anomaly detected</p>
              <p>⚡ Unusual pattern in signals</p>
              <p>⚡ Requires investigation</p>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default LightBulbVisualization

