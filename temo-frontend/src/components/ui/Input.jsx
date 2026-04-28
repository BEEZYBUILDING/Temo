import React from 'react'

export default function Input({ label, error, className = '', ...props }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-xs uppercase tracking-widest text-stone-400">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-3 rounded-sm transition-colors ${className}`}
        {...props}
      />
      {error && (
        <p className="text-xs text-red-400 mt-0.5">{error}</p>
      )}
    </div>
  )
}
