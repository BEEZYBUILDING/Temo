import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCartStore } from '../store/cartStore'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../api/auth'
import { ordersApi } from '../api/orders'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import toast from 'react-hot-toast'
import { ShoppingBag, Lock } from 'lucide-react'

export default function CheckoutPage() {
  const { cart, fetchCart, clearCart } = useCartStore()
  const { isAuthenticated } = useAuthStore()
  const navigate = useNavigate()
  const [addresses, setAddresses] = useState([])
  const [selectedAddress, setSelectedAddress] = useState(null)
  const [newAddress, setNewAddress] = useState({ street: '', city: '', state: '', postal_code: '' })
  const [useNew, setUseNew] = useState(false)
  const [placing, setPlacing] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login', { state: { from: { pathname: '/checkout' } } }); return }
    fetchCart()
    authApi.getAddresses().then(({ data }) => {
      setAddresses(data)
      if (data.length > 0) setSelectedAddress(data[0])
      else setUseNew(true)
    }).catch(() => setUseNew(true))
  }, [])

  const items = cart?.items || []
  const subtotal = parseFloat(cart?.subtotal || 0)
  const shipping = subtotal > 150 ? 0 : 10
  const total = subtotal + shipping

  const handlePlaceOrder = async () => {
    const address = useNew ? newAddress : selectedAddress
    if (!address) { toast.error('Please select or enter an address'); return }

    setPlacing(true)
    try {
      await ordersApi.create({ address })
      await clearCart()
      toast.success('Order placed successfully!')
      navigate('/orders')
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed to place order')
    } finally {
      setPlacing(false)
    }
  }

  if (items.length === 0) {
    return (
      <div className="min-h-screen pt-20 flex flex-col items-center justify-center gap-4">
        <ShoppingBag size={48} className="text-stone-700" />
        <p className="serif text-2xl text-stone-500">Your cart is empty</p>
        <button onClick={() => navigate('/products')} className="text-amber-500 text-sm hover:text-amber-400">
          Continue Shopping →
        </button>
      </div>
    )
  }

  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-6xl mx-auto px-6 py-10">
        <h1 className="serif text-4xl font-light text-stone-100 mb-10">Checkout</h1>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-10">
          {/* Left: Address */}
          <div className="lg:col-span-3 space-y-6">
            <div className="border border-stone-800 rounded-sm p-6 space-y-5">
              <h2 className="serif text-xl text-stone-200">Delivery Address</h2>

              {addresses.length > 0 && (
                <div className="space-y-3">
                  {addresses.map(addr => (
                    <label
                      key={addr.id}
                      className={`flex items-start gap-3 p-4 border rounded-sm cursor-pointer transition-colors ${
                        !useNew && selectedAddress?.id === addr.id
                          ? 'border-amber-600 bg-amber-950/20'
                          : 'border-stone-800 hover:border-stone-700'
                      }`}
                    >
                      <input
                        type="radio"
                        checked={!useNew && selectedAddress?.id === addr.id}
                        onChange={() => { setSelectedAddress(addr); setUseNew(false) }}
                        className="mt-0.5 accent-amber-500"
                      />
                      <div>
                        <p className="text-sm text-stone-200">{addr.street}</p>
                        <p className="text-sm text-stone-400">{addr.city}, {addr.state} {addr.postal_code}</p>
                      </div>
                    </label>
                  ))}
                  <label className={`flex items-center gap-3 p-4 border rounded-sm cursor-pointer transition-colors ${
                    useNew ? 'border-amber-600 bg-amber-950/20' : 'border-stone-800 hover:border-stone-700'
                  }`}>
                    <input
                      type="radio"
                      checked={useNew}
                      onChange={() => setUseNew(true)}
                      className="accent-amber-500"
                    />
                    <span className="text-sm text-stone-300">Use a new address</span>
                  </label>
                </div>
              )}

              {(useNew || addresses.length === 0) && (
                <div className="grid grid-cols-2 gap-4 pt-2 animate-fade">
                  <Input label="Street" className="col-span-2" value={newAddress.street} onChange={e => setNewAddress(a => ({...a, street: e.target.value}))} placeholder="123 Main St" />
                  <Input label="City" value={newAddress.city} onChange={e => setNewAddress(a => ({...a, city: e.target.value}))} placeholder="New York" />
                  <Input label="State" value={newAddress.state} onChange={e => setNewAddress(a => ({...a, state: e.target.value}))} placeholder="NY" />
                  <Input label="Postal Code" value={newAddress.postal_code} onChange={e => setNewAddress(a => ({...a, postal_code: e.target.value}))} placeholder="10001" className="col-span-2" />
                </div>
              )}
            </div>
          </div>

          {/* Right: Summary */}
          <div className="lg:col-span-2">
            <div className="border border-stone-800 rounded-sm p-6 space-y-5 sticky top-24">
              <h2 className="serif text-xl text-stone-200">Order Summary</h2>

              <div className="space-y-3 max-h-48 overflow-y-auto">
                {items.map(item => (
                  <div key={item.variant_id} className="flex items-center justify-between text-sm">
                    <div>
                      <p className="text-stone-200 truncate max-w-[160px]">{item.product_name}</p>
                      <p className="text-stone-500 text-xs">×{item.quantity}</p>
                    </div>
                    <p className="mono text-stone-300">${parseFloat(item.line_total).toFixed(2)}</p>
                  </div>
                ))}
              </div>

              <hr className="border-stone-800" />

              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-stone-400">
                  <span>Subtotal</span>
                  <span className="mono">${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-stone-400">
                  <span>Shipping</span>
                  <span className="mono">{shipping === 0 ? 'Free' : `$${shipping.toFixed(2)}`}</span>
                </div>
              </div>

              <hr className="border-stone-800" />

              <div className="flex justify-between">
                <span className="text-stone-200 font-medium uppercase text-xs tracking-widest">Total</span>
                <span className="serif text-2xl text-amber-400">${total.toFixed(2)}</span>
              </div>

              <Button fullWidth size="lg" onClick={handlePlaceOrder} loading={placing}>
                <Lock size={14} />
                Place Order
              </Button>

              <p className="text-xs text-stone-600 text-center flex items-center justify-center gap-1">
                <Lock size={10} /> Secure checkout
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
