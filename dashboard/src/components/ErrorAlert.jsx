import React from 'react'
import { AlertCircle, X } from 'lucide-react'

function ErrorAlert({ message, onDismiss }) {
  return (
    <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-start gap-4 animate-fade-in">
      <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <h3 className="font-semibold text-red-400 mb-1">Prediction Error</h3>
        <p className="text-sm text-red-300">{message}</p>
      </div>
      <button
        onClick={onDismiss}
        className="text-red-400 hover:text-red-300 transition-colors p-1"
        aria-label="Dismiss error"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  )
}

export default ErrorAlert

