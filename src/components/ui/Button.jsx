import React from 'react'

const variants = {
  primary: {
    base: 'bg-amber-600 text-stone-950 hover:bg-amber-500',
    border: '',
  },
  secondary: {
    base: 'bg-transparent text-amber-500 hover:bg-stone-800',
    border: 'border border-stone-700 hover:border-amber-600',
  },
  ghost: {
    base: 'bg-transparent text-stone-400 hover:text-stone-100 hover:bg-stone-800',
    border: '',
  },
  danger: {
    base: 'bg-red-900/40 text-red-400 hover:bg-red-900/60',
    border: 'border border-red-900/50',
  },
}

const sizes = {
  sm: 'px-3 py-1.5 text-xs tracking-wider',
  md: 'px-5 py-2.5 text-sm tracking-wider',
  lg: 'px-8 py-3.5 text-sm tracking-widest',
}

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  loading = false,
  disabled = false,
  fullWidth = false,
  ...props
}) {
  const v = variants[variant]

  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2 uppercase font-medium
        transition-all duration-200 rounded-sm
        ${v.base} ${v.border} ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''}
        ${className}
      `}
    >
      {loading && (
        <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full spin" />
      )}
      {children}
    </button>
  )
}
