import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import toast from 'react-hot-toast'

export default function RegisterPage() {
  const { register, loading } = useAuthStore()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email:'', password:'', password2:'', first_name:'', last_name:'' })
  const [errors, setErrors] = useState({})

  const handleSubmit = async (e) => {
    e.preventDefault(); setErrors({})
    if (form.password !== form.password2) { setErrors({ password2: ['Passwords do not match'] }); return }
    try {
      await register(form)
      toast.success('Account created! Please sign in.')
      navigate('/login')
    } catch (err) {
      const data = err.response?.data
      if (data) setErrors(data)
      toast.error('Registration failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-20">
      <div className="w-full max-w-sm">
        <div className="mb-10">
          <Link to="/" className="serif text-2xl text-amber-400 block mb-8">TEMO</Link>
          <h1 className="serif text-3xl font-light text-stone-100 mb-2">Create Account</h1>
          <p className="text-sm text-stone-500">Already have one? <Link to="/login" className="text-amber-500 hover:text-amber-400">Sign In</Link></p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="First Name" placeholder="Jane" required value={form.first_name} onChange={e => setForm(f => ({...f,first_name:e.target.value}))} error={errors.first_name?.[0]} />
            <Input label="Last Name" placeholder="Doe" value={form.last_name} onChange={e => setForm(f => ({...f,last_name:e.target.value}))} error={errors.last_name?.[0]} />
          </div>
          <Input label="Email" type="email" placeholder="you@example.com" required value={form.email} onChange={e => setForm(f => ({...f,email:e.target.value}))} error={errors.email?.[0]} />
          <Input label="Password" type="password" placeholder="••••••••" required value={form.password} onChange={e => setForm(f => ({...f,password:e.target.value}))} error={errors.password?.[0]} />
          <Input label="Confirm Password" type="password" placeholder="••••••••" required value={form.password2} onChange={e => setForm(f => ({...f,password2:e.target.value}))} error={errors.password2?.[0]} />
          <Button type="submit" fullWidth size="lg" loading={loading} className="mt-4">Create Account</Button>
        </form>
      </div>
    </div>
  )
}
