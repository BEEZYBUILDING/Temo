import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ShoppingBag, ChevronLeft, ChevronRight, Minus, Plus } from 'lucide-react'
import { productsApi } from '../api/products'
import { useCartStore } from '../store/cartStore'
import Button from '../components/ui/Button'
import toast from 'react-hot-toast'

export default function ProductDetailPage() {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedVariant, setSelectedVariant] = useState(null)
  const [quantity, setQuantity] = useState(1)
  const [activeImage, setActiveImage] = useState(0)
  const [adding, setAdding] = useState(false)
  const { addItem } = useCartStore()

  useEffect(() => {
    setLoading(true)
    productsApi.detail(id)
      .then(({ data }) => {
        setProduct(data)
        setSelectedVariant(data.variants?.find(v => v.in_stock) || data.variants?.[0] || null)
      })
      .catch(() => setProduct(null))
      .finally(() => setLoading(false))
  }, [id])

  const handleAddToCart = async () => {
    if (!selectedVariant) return
    setAdding(true)
    try {
      await addItem(selectedVariant.id, quantity)
      toast.success(`Added ${quantity}× to cart`)
    } catch (e) {
      toast.error(e.response?.data?.error || 'Could not add to cart')
    } finally { setAdding(false) }
  }

  if (loading) return (
    <div className="min-h-screen pt-20 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full spin" />
    </div>
  )

  if (!product) return (
    <div className="min-h-screen pt-20 flex flex-col items-center justify-center gap-4">
      <p className="serif text-4xl text-stone-600">Product not found</p>
      <Link to="/products" className="text-amber-500 text-sm hover:text-amber-400">← Back to shop</Link>
    </div>
  )

  const images = product.images || []

  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <nav className="flex items-center gap-2 text-xs text-stone-500">
          <Link to="/" className="hover:text-stone-300">Home</Link>
          <span>/</span>
          <Link to="/products" className="hover:text-stone-300">Shop</Link>
          <span>/</span>
          <span className="text-stone-300">{product.name}</span>
        </nav>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <div className="space-y-4">
            <div className="relative aspect-square bg-stone-900 rounded-sm overflow-hidden">
              {images[activeImage] ? (
                <img src={images[activeImage].url} alt={product.name} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <ShoppingBag size={64} className="text-stone-700" />
                </div>
              )}
              {images.length > 1 && (
                <>
                  <button onClick={() => setActiveImage(i => Math.max(0,i-1))}
                    className="absolute left-3 top-1/2 -translate-y-1/2 p-2 bg-stone-950/80 text-stone-300 hover:text-stone-100 rounded-sm">
                    <ChevronLeft size={18} />
                  </button>
                  <button onClick={() => setActiveImage(i => Math.min(images.length-1,i+1))}
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-stone-950/80 text-stone-300 hover:text-stone-100 rounded-sm">
                    <ChevronRight size={18} />
                  </button>
                </>
              )}
            </div>
            {images.length > 1 && (
              <div className="flex gap-3 overflow-x-auto pb-2">
                {images.map((img,i) => (
                  <button key={img.id} onClick={() => setActiveImage(i)}
                    className={`flex-shrink-0 w-20 h-20 rounded-sm overflow-hidden border-2 transition-colors ${i===activeImage?'border-amber-500':'border-transparent'}`}>
                    <img src={img.url} alt="" className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="space-y-8">
            <div>
              <p className="text-xs text-stone-500 uppercase tracking-widest mb-2">{product.category_name || 'Uncategorized'}</p>
              <h1 className="serif text-4xl font-light text-stone-100 mb-4">{product.name}</h1>
              {selectedVariant && <p className="mono text-2xl text-amber-400">${parseFloat(selectedVariant.price).toFixed(2)}</p>}
            </div>

            {product.description && <p className="text-stone-400 leading-relaxed text-sm">{product.description}</p>}

            {product.variants?.length > 1 && (
              <div className="space-y-3">
                <p className="text-xs uppercase tracking-widest text-stone-400">Select Variant</p>
                <div className="flex flex-wrap gap-2">
                  {product.variants.map(v => (
                    <button key={v.id} onClick={() => setSelectedVariant(v)} disabled={!v.in_stock}
                      className={`px-4 py-2.5 rounded-sm text-xs uppercase tracking-wider border transition-all ${
                        selectedVariant?.id===v.id ? 'border-amber-500 bg-amber-950/30 text-amber-400'
                        : v.in_stock ? 'border-stone-700 text-stone-300 hover:border-stone-500'
                        : 'border-stone-800 text-stone-600 cursor-not-allowed line-through'
                      }`}>
                      {v.sku}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-4 pt-2">
              <div className="flex items-center gap-4">
                <div className="flex items-center border border-stone-700 rounded-sm">
                  <button onClick={() => setQuantity(q => Math.max(1,q-1))} className="px-4 py-3 text-stone-400 hover:text-stone-100"><Minus size={14} /></button>
                  <span className="px-6 text-stone-200 mono">{quantity}</span>
                  <button onClick={() => setQuantity(q => q+1)} className="px-4 py-3 text-stone-400 hover:text-stone-100"><Plus size={14} /></button>
                </div>
                {selectedVariant?.in_stock
                  ? <span className="text-xs text-green-500 uppercase tracking-widest">In Stock</span>
                  : <span className="text-xs text-red-400 uppercase tracking-widest">Out of Stock</span>}
              </div>
              <Button fullWidth size="lg" onClick={handleAddToCart} loading={adding} disabled={!selectedVariant?.in_stock}>
                <ShoppingBag size={16} /> Add to Cart
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
