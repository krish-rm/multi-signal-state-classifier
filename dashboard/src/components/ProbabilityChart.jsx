import React, { useMemo } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts'

const stateColors = {
  calm: '#3B82F6',
  alert: '#F59E0B',
  risk: '#EF4444',
  flow: '#10B981',
  deviation: '#8B5CF6',
}

function ProbabilityChart({ probabilities }) {
  const chartData = useMemo(() => {
    return Object.entries(probabilities || {}).map(([state, probability]) => ({
      name: state.charAt(0).toUpperCase() + state.slice(1),
      probability: (probability * 100).toFixed(1),
      fullProbability: probability,
    }))
  }, [probabilities])

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800 border border-slate-600 rounded px-3 py-2 shadow-lg">
          <p className="text-white font-semibold">{payload[0].payload.name}</p>
          <p className="text-blue-400 text-sm">
            {payload[0].payload.probability}%
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="space-y-2">
      {/* Chart */}
      <div className="bg-slate-700/30 rounded-lg p-2 border border-slate-600">
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={chartData}>
            <defs>
              {Object.entries(stateColors).map(([state, color]) => (
                <linearGradient
                  key={`gradient-${state}`}
                  id={`gradient-${state}`}
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop offset="0%" stopColor={color} stopOpacity={0.9} />
                  <stop offset="100%" stopColor={color} stopOpacity={0.6} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis
              dataKey="name"
              stroke="#94A3B8"
              style={{ fontSize: '10px' }}
              tick={{ fill: '#E2E8F0' }}
            />
            <YAxis
              stroke="#94A3B8"
              style={{ fontSize: '10px' }}
              domain={[0, 100]}
              tick={{ fill: '#E2E8F0' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="probability" radius={[8, 8, 0, 0]} isAnimationActive>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={`url(#gradient-${entry.name.toLowerCase()})`}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Probability Breakdown */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2">
        {chartData.map((item) => {
          const state = item.name.toLowerCase()
          const color = stateColors[state]
          return (
            <div
              key={state}
              className="p-2 bg-slate-700/50 rounded-lg border border-slate-600 text-center"
            >
              <p className="text-xs text-slate-400 uppercase tracking-wide font-semibold mb-0.5">
                {item.name}
              </p>
              <div className="flex items-center justify-center gap-1.5">
                <div
                  className="w-2.5 h-2.5 rounded-full"
                  style={{ backgroundColor: color }}
                ></div>
                <p className="text-lg font-bold text-white">
                  {item.probability}%
                </p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Info */}
      <div className="p-2 bg-blue-500/10 border border-blue-500/20 rounded-lg">
        <p className="text-xs text-slate-300">
          <span className="font-semibold text-blue-400">ℹ️</span> Confidence scores for each state.
        </p>
      </div>
    </div>
  )
}

export default ProbabilityChart

