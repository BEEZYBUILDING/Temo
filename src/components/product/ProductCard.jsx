import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { ShoppingBag, Eye } from 'lucide-react'
import { useCartStore } from '../../store/cartStore'
import toast from 'react-hot-toast'

export default function ProductCard({ product }) {
  const { addItem } = useCartStore()
  const [adding, setAdding] = useState(false)

  const primaryImage = product.images?.find(i => i.is_primary) || product.images?.[0]
  const lowestVariant = product.variants?.reduce((min, v) =>
    parseFloat(v.price) < parseFloat(min?.price || Infinity) ? v : min, null)
  const inStock = product.variants?.some(v => v.in_stock)

  const handleQuickAdd = async (e) => {
    e.preventDefault()
    if (!lowestVariant || !inStock) return
    setAdding(true)
    try {
      await addItem(lowestVariant.id)
      toast.success('Added to cart')
    } catch {
      toast.error('Could not add to cart')
    } finally {
      setAdding(false)
    }
  }

  return (
    <Link to={`/products/${product.id}`} className="group block">
      {/* Image */}
      <div className="relative aspect-[3/4] bg-stone-900 overflow-hidden rounded-sm mb-4">
        {primaryImage ? (
          <img
            src={primaryImage.url}
            alt={product.name}
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <ShoppingBag size={32} className="text-stone-700" />
          </div>
        )}

        {/* Overlay actions */}
        <div className="absolute inset-0 bg-stone-950/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4 gap-2">
          <button
            onClick={handleQuickAdd}
            disabled={!inStock || adding}
            className="flex items-center gap-2 px-4 py-2.5 bg-stone-950/90 text-amber-400 text-xs uppercase tracking-widest border border-amber-700/50 hover:bg-amber-500 hover:text-stone-950 hover:border-amber-500 transition-all duration-200 rounded-sm disabled:opacity-50"
          >
            {adding ? (
              <span className="w-3 h-3 border border-current border-t-transparent rounded-full spin" />
            ) : (
              <ShoppingBag size={12} />
            )}
            {inStock ? 'Add to Cart' : 'Out of Stock'}
          </button>
        </div>

        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-1">
          {!inStock && (
            <span className="px-2 py-1 bg-stone-800/90 text-stone-400 text-[10px] uppercase tracking-widest">
              Sold Out
            </span>
          )}
        </div>
      </div>

      {/* Info */}
      <div className="space-y-1">
        <p className="text-xs text-stone-500 uppercase tracking-widest">
          {product.category_name || 'Uncategorized'}
        </p>
        <h3 className="text-stone-100 text-sm group-hover:text-amber-400 transition-colors">
          {product.name}
        </h3>
        {lowestVariant && (
          <p className="mono text-sm text-stone-300">
            ${parseFloat(lowestVariant.price).toFixed(2)}
          </p>
        )}
      </div>
    </Link>
  )
}
