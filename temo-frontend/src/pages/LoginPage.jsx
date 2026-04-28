import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import toast from 'react-hot-toast'

export default function LoginPage() {
  const { login, loading } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()
  const [form, setForm] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState({})
  const from = location.state?.from?.pathname || '/'

  const handleSubmit = async (e) => {
    e.preventDefault(); setErrors({})
    try {
      await login(form)
      toast.success('Welcome back!')
      navigate(from, { replace: true })
    } catch (err) {
      const data = err.response?.data
      if (data) setErrors(data)
      toast.error(data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex">
      <div className="hidden lg:flex flex-1 items-center justify-center bg-stone-900 relative overflow-hidden">
        <div className="absolute inset-0 opacity-[0.04]" style={{backgroundImage:'linear-gradient(#2a2520 1px,transparent 1px),linear-gradient(90deg,#2a2520 1px,transparent 1px)',backgroundSize:'40px 40px'}} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-amber-600/8 rounded-full blur-[80px]" />
        <div className="text-center relative z-10">
          <p className="mono text-xs text-amber-500 tracking-[0.3em] mb-4">TEMO</p>
          <h2 className="serif text-5xl font-light text-stone-200 leading-tight">Welcome<br /><span className="italic">back.</span></h2>
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center px-8 py-20">
        <div className="w-full max-w-sm">
          <div className="mb-10">
            <Link to="/" className="serif text-2xl text-amber-400 block mb-8">TEMO</Link>
            <h1 className="serif text-3xl font-light text-stone-100 mb-2">Sign In</h1>
            <p className="text-sm text-stone-500">Don't have an account? <Link to="/register" className="text-amber-500 hover:text-amber-400">Register</Link></p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input label="Email" type="email" value={form.email} onChange={e => setForm(f => ({...f,email:e.target.value}))} placeholder="you@example.com" required error={errors.email?.[0]} />
            <Input label="Password" type="password" value={form.password} onChange={e => setForm(f => ({...f,password:e.target.value}))} placeholder="••••••••" required error={errors.password?.[0]} />
            {errors.detail && <p className="text-xs text-red-400 text-center">{errors.detail}</p>}
            <Button type="submit" fullWidth size="lg" loading={loading} className="mt-6">Sign In</Button>
          </form>
        </div>
      </div>
    </div>
  )
}
