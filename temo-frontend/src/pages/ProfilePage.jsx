import React, { useState, useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../api/auth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import toast from 'react-hot-toast'
import { User, MapPin, Lock, Plus, Trash2, Edit2, Check, X } from 'lucide-react'

function AddressCard({ address, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState(address)

  const handleSave = async () => {
    try {
      await onUpdate(address.id, form)
      setEditing(false)
      toast.success('Address updated')
    } catch {
      toast.error('Failed to update')
    }
  }

  if (editing) {
    return (
      <div className="border border-amber-700/50 bg-amber-950/10 rounded-sm p-4 space-y-3 animate-fade">
        <div className="grid grid-cols-2 gap-3">
          <Input placeholder="Street" value={form.street} onChange={e => setForm(f => ({...f, street: e.target.value}))} />
          <Input placeholder="City" value={form.city} onChange={e => setForm(f => ({...f, city: e.target.value}))} />
          <Input placeholder="State" value={form.state} onChange={e => setForm(f => ({...f, state: e.target.value}))} />
          <Input placeholder="Postal Code" value={form.postal_code} onChange={e => setForm(f => ({...f, postal_code: e.target.value}))} />
        </div>
        <div className="flex gap-2">
          <Button size="sm" onClick={handleSave}><Check size={12} /> Save</Button>
          <Button size="sm" variant="ghost" onClick={() => setEditing(false)}><X size={12} /> Cancel</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="border border-stone-800 rounded-sm p-4 flex items-start justify-between group">
      <div className="space-y-1">
        <p className="text-sm text-stone-200">{address.street}</p>
        <p className="text-sm text-stone-400">{address.city}, {address.state} {address.postal_code}</p>
        {address.is_default && (
          <span className="text-[10px] text-amber-500 uppercase tracking-widest">Default</span>
        )}
      </div>
      <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <button onClick={() => setEditing(true)} className="p-1.5 text-stone-500 hover:text-stone-200">
          <Edit2 size={14} />
        </button>
        <button onClick={() => onDelete(address.id)} className="p-1.5 text-stone-500 hover:text-red-400">
          <Trash2 size={14} />
        </button>
      </div>
    </div>
  )
}

export default function ProfilePage() {
  const { user, initialize } = useAuthStore()
  const [tab, setTab] = useState('profile')
  const [profileForm, setProfileForm] = useState({ first_name: '', last_name: '', email: '' })
  const [passwordForm, setPasswordForm] = useState({ old_password: '', new_password: '', confirm_password: '' })
  const [addresses, setAddresses] = useState([])
  const [newAddress, setNewAddress] = useState(null)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (user) setProfileForm({ first_name: user.first_name || '', last_name: user.last_name || '', email: user.email })
    loadAddresses()
  }, [user])

  const loadAddresses = async () => {
    try {
      const { data } = await authApi.getAddresses()
      setAddresses(data)
    } catch {}
  }

  const handleProfileSave = async () => {
    setSaving(true)
    try {
      await authApi.updateMe(profileForm)
      await initialize()
      toast.success('Profile updated')
    } catch {
      toast.error('Failed to update')
    } finally {
      setSaving(false)
    }
  }

  const handlePasswordChange = async () => {
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      toast.error('Passwords do not match')
      return
    }
    setSaving(true)
    try {
      await authApi.changePassword({ old_password: passwordForm.old_password, new_password: passwordForm.new_password })
      setPasswordForm({ old_password: '', new_password: '', confirm_password: '' })
      toast.success('Password changed')
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed to change password')
    } finally {
      setSaving(false)
    }
  }

  const handleAddAddress = async () => {
    try {
      await authApi.createAddress(newAddress)
      await loadAddresses()
      setNewAddress(null)
      toast.success('Address added')
    } catch {
      toast.error('Failed to add address')
    }
  }

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'addresses', label: 'Addresses', icon: MapPin },
    { id: 'security', label: 'Security', icon: Lock },
  ]

  return (
    <div className="min-h-screen pt-24 max-w-4xl mx-auto px-6 pb-16">
      <h1 className="serif text-4xl font-light text-stone-100 mb-8">My Account</h1>

      <div className="flex gap-8">
        {/* Tabs */}
        <aside className="w-48 flex-shrink-0 space-y-1">
          {tabs.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setTab(id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-sm text-sm transition-colors ${
                tab === id
                  ? 'bg-amber-950/30 text-amber-400 border border-amber-700/50'
                  : 'text-stone-400 hover:text-stone-200 hover:bg-stone-900'
              }`}
            >
              <Icon size={14} />
              {label}
            </button>
          ))}
        </aside>

        {/* Content */}
        <div className="flex-1 animate-fade">
          {tab === 'profile' && (
            <div className="space-y-5 border border-stone-800 rounded-sm p-6">
              <h2 className="serif text-xl text-stone-200">Personal Information</h2>
              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="First Name"
                  value={profileForm.first_name}
                  onChange={e => setProfileForm(f => ({...f, first_name: e.target.value}))}
                />
                <Input
                  label="Last Name"
                  value={profileForm.last_name}
                  onChange={e => setProfileForm(f => ({...f, last_name: e.target.value}))}
                />
              </div>
              <Input
                label="Email"
                type="email"
                value={profileForm.email}
                onChange={e => setProfileForm(f => ({...f, email: e.target.value}))}
              />
              <Button onClick={handleProfileSave} loading={saving}>Save Changes</Button>
            </div>
          )}

          {tab === 'addresses' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="serif text-xl text-stone-200">Saved Addresses</h2>
                <Button size="sm" variant="secondary" onClick={() => setNewAddress({ street: '', city: '', state: '', postal_code: '' })}>
                  <Plus size={14} /> Add New
                </Button>
              </div>

              {newAddress && (
                <div className="border border-amber-700/50 bg-amber-950/10 rounded-sm p-4 space-y-3 animate-fade">
                  <div className="grid grid-cols-2 gap-3">
                    <Input placeholder="Street" value={newAddress.street} onChange={e => setNewAddress(a => ({...a, street: e.target.value}))} />
                    <Input placeholder="City" value={newAddress.city} onChange={e => setNewAddress(a => ({...a, city: e.target.value}))} />
                    <Input placeholder="State" value={newAddress.state} onChange={e => setNewAddress(a => ({...a, state: e.target.value}))} />
                    <Input placeholder="Postal Code" value={newAddress.postal_code} onChange={e => setNewAddress(a => ({...a, postal_code: e.target.value}))} />
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" onClick={handleAddAddress}><Check size={12} /> Save</Button>
                    <Button size="sm" variant="ghost" onClick={() => setNewAddress(null)}><X size={12} /> Cancel</Button>
                  </div>
                </div>
              )}

              {addresses.length === 0 && !newAddress ? (
                <p className="text-sm text-stone-500 py-8 text-center">No saved addresses</p>
              ) : (
                addresses.map(addr => (
                  <AddressCard
                    key={addr.id}
                    address={addr}
                    onUpdate={async (id, data) => { await authApi.updateAddress(id, data); await loadAddresses() }}
                    onDelete={async (id) => { await authApi.deleteAddress(id); await loadAddresses(); toast.success('Removed') }}
                  />
                ))
              )}
            </div>
          )}

          {tab === 'security' && (
            <div className="space-y-5 border border-stone-800 rounded-sm p-6">
              <h2 className="serif text-xl text-stone-200">Change Password</h2>
              <Input
                label="Current Password"
                type="password"
                value={passwordForm.old_password}
                onChange={e => setPasswordForm(f => ({...f, old_password: e.target.value}))}
              />
              <Input
                label="New Password"
                type="password"
                value={passwordForm.new_password}
                onChange={e => setPasswordForm(f => ({...f, new_password: e.target.value}))}
              />
              <Input
                label="Confirm New Password"
                type="password"
                value={passwordForm.confirm_password}
                onChange={e => setPasswordForm(f => ({...f, confirm_password: e.target.value}))}
              />
              <Button onClick={handlePasswordChange} loading={saving}>Update Password</Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
