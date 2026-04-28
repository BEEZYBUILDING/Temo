import React, { useEffect } from 'react'
import { X, Plus, Minus, Trash2, ShoppingBag, ArrowRight } from 'lucide-react'
import { useCartStore } from '../../store/cartStore'
import { Link } from 'react-router-dom'
import Button from '../ui/Button'

function CartItem({ item, onUpdate, onRemove }) {
  return (
    <div className="flex gap-4 py-5 border-b border-stone-800 animate-fade">
      {/* Image placeholder */}
      <div className="w-16 h-20 bg-stone-800 rounded-sm flex-shrink-0 flex items-center justify-center">
        {item.image ? (
          <img src={item.image} alt={item.name} className="w-full h-full object-cover rounded-sm" />
        ) : (
          <ShoppingBag size={20} className="text-stone-600" />
        )}
      </div>

      <div className="flex-1 min-w-0">
        <h4 className="text-sm text-stone-100 truncate">{item.product_name}</h4>
        {item.attributes && (
          <p className="text-xs text-stone-500 mt-0.5 truncate">
            {Object.entries(item.attributes).map(([k, v]) => `${k}: ${v}`).join(' · ')}
          </p>
        )}
        <p className="text-xs text-amber-500 mono mt-1">${parseFloat(item.unit_price).toFixed(2)}</p>

        <div className="flex items-center gap-3 mt-3">
          <div className="flex items-center border border-stone-700 rounded-sm">
            <button
              onClick={() => onUpdate(item.variant_id, item.quantity - 1)}
              className="px-2 py-1 text-stone-400 hover:text-stone-100"
            >
              <Minus size={12} />
            </button>
            <span className="px-3 text-sm mono text-stone-200">{item.quantity}</span>
            <button
              onClick={() => onUpdate(item.variant_id, item.quantity + 1)}
              className="px-2 py-1 text-stone-400 hover:text-stone-100"
            >
              <Plus size={12} />
            </button>
          </div>
          <button
            onClick={() => onRemove(item.variant_id)}
            className="text-stone-600 hover:text-red-400 transition-colors"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <div className="text-sm mono text-stone-200 flex-shrink-0">
        ${parseFloat(item.line_total).toFixed(2)}
      </div>
    </div>
  )
}

export default function CartDrawer() {
  const { open, setOpen, cart, loading, fetchCart, updateItem, removeItem, clearCart } = useCartStore()

  useEffect(() => {
    if (open) fetchCart()
  }, [open])

  const items = cart?.items || []
  const subtotal = cart?.subtotal || 0

  return (
    <>
      {/* Backdrop */}
      {open && (
        <div
          className="fixed inset-0 bg-black/60 z-50 backdrop-blur-sm"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Drawer */}
      <div
        className={`fixed top-0 right-0 h-full w-full max-w-md bg-stone-950 border-l border-stone-800 z-50 flex flex-col transition-transform duration-300 ease-out ${
          open ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-stone-800">
          <div className="flex items-center gap-3">
            <h2 className="serif text-2xl font-light text-stone-100">Cart</h2>
            {items.length > 0 && (
              <span className="text-xs text-stone-500 mono">({items.length} items)</span>
            )}
          </div>
          <button
            onClick={() => setOpen(false)}
            className="text-stone-500 hover:text-stone-100 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Items */}
        <div className="flex-1 overflow-y-auto px-6">
          {loading ? (
            <div className="flex items-center justify-center h-40">
              <div className="w-6 h-6 border-2 border-amber-500 border-t-transparent rounded-full spin" />
            </div>
          ) : items.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 gap-4">
              <ShoppingBag size={40} className="text-stone-700" />
              <p className="text-stone-500 text-sm">Your cart is empty</p>
              <button
                onClick={() => setOpen(false)}
                className="text-xs uppercase tracking-widest text-amber-500 hover:text-amber-400"
              >
                Continue Shopping →
              </button>
            </div>
          ) : (
            items.map((item) => (
              <CartItem
                key={item.variant_id}
                item={item}
                onUpdate={updateItem}
                onRemove={removeItem}
              />
            ))
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && (
          <div className="px-6 py-6 border-t border-stone-800 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-stone-400 uppercase tracking-widest">Subtotal</span>
              <span className="serif text-2xl text-stone-100">${parseFloat(subtotal).toFixed(2)}</span>
            </div>
            <p className="text-xs text-stone-600">Shipping & taxes calculated at checkout</p>
            <Link to="/checkout" onClick={() => setOpen(false)}>
              <Button fullWidth size="lg" className="group">
                Checkout
                <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <button
              onClick={clearCart}
              className="w-full text-xs text-stone-600 hover:text-red-400 transition-colors uppercase tracking-widest"
            >
              Clear cart
            </button>
          </div>
        )}
      </div>
    </>
  )
}
