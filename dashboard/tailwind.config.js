export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary colors from PRD
        calm: '#3B82F6',      // Blue
        alert: '#F59E0B',     // Amber
        risk: '#EF4444',      // Red
        flow: '#10B981',      // Green
        deviation: '#8B5CF6', // Purple
        
        // Neutral palette
        'slate-50': '#F8FAFC',
        'slate-100': '#F1F5F9',
        'slate-200': '#E2E8F0',
        'slate-300': '#CBD5E1',
        'slate-400': '#94A3B8',
        'slate-500': '#64748B',
        'slate-600': '#475569',
        'slate-700': '#334155',
        'slate-800': '#1E293B',
        'slate-900': '#0F172A',
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-fast': 'pulse 0.6s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-light': 'bounce 1s infinite',
        'glow': 'glow 1.5s ease-in-out infinite',
        'flash': 'flash 0.5s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%, 100%': { opacity: 1, filter: 'drop-shadow(0 0 10px)' },
          '50%': { opacity: 0.7, filter: 'drop-shadow(0 0 20px)' },
        },
        flash: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.3 },
        },
      },
      transitionProperty: {
        'colors': 'color, background-color, border-color, text-decoration-color, fill, stroke',
      },
    },
  },
  plugins: [],
}

