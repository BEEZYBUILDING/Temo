import React, { useState, useEffect, useCallback } from 'react'
import { Search, SlidersHorizontal, ChevronDown } from 'lucide-react'
import { productsApi } from '../api/products'
import ProductCard from '../components/product/ProductCard'

export default function ProductsPage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [ordering, setOrdering] = useState('-created_at')
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState({ min_price: '', max_price: '', in_stock: false })

  const fetchProducts = useCallback(async () => {
    setLoading(true)
    try {
      const params = { search: search || undefined, ordering }
      if (filters.min_price) params.min_price = filters.min_price
      if (filters.max_price) params.max_price = filters.max_price
      if (filters.in_stock) params.in_stock = true
      const { data } = await productsApi.list(params)
      setProducts(data.results || data)
    } catch { setProducts([]) }
    finally { setLoading(false) }
  }, [search, ordering, filters])

  useEffect(() => {
    const t = setTimeout(fetchProducts, 350)
    return () => clearTimeout(t)
  }, [fetchProducts])

  return (
    <div className="min-h-screen pt-20">
      <div className="border-b border-stone-800 bg-stone-950/50">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <h1 className="serif text-4xl font-light text-stone-100 mb-6">Shop</h1>
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            <div className="relative flex-1 max-w-md">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-500" />
              <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search products..."
                className="w-full pl-10 pr-4 py-3 rounded-sm text-sm" />
            </div>
            <div className="flex items-center gap-3">
              <button onClick={() => setShowFilters(!showFilters)}
                className={`flex items-center gap-2 px-4 py-3 border rounded-sm text-xs uppercase tracking-widest transition-colors ${showFilters ? 'border-amber-600 text-amber-400' : 'border-stone-700 text-stone-400 hover:border-stone-500'}`}>
                <SlidersHorizontal size={14} /> Filters
              </button>
              <div className="relative">
                <select value={ordering} onChange={e => setOrdering(e.target.value)}
                  className="appearance-none pl-4 pr-8 py-3 rounded-sm text-xs uppercase tracking-widest cursor-pointer">
                  <option value="-created_at">Newest</option>
                  <option value="price">Price: Low–High</option>
                  <option value="-price">Price: High–Low</option>
                  <option value="name">Name A–Z</option>
                </select>
                <ChevronDown size={12} className="absolute right-2.5 top-1/2 -translate-y-1/2 text-stone-500 pointer-events-none" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex gap-8">
          {showFilters && (
            <aside className="w-56 flex-shrink-0 space-y-6">
              <div>
                <p className="text-xs uppercase tracking-widest text-stone-500 mb-3">Price Range</p>
                <div className="flex gap-2">
                  <input placeholder="Min" type="number" value={filters.min_price}
                    onChange={e => setFilters(f => ({...f, min_price: e.target.value}))}
                    className="flex-1 px-3 py-2 rounded-sm text-sm" />
                  <input placeholder="Max" type="number" value={filters.max_price}
                    onChange={e => setFilters(f => ({...f, max_price: e.target.value}))}
                    className="flex-1 px-3 py-2 rounded-sm text-sm" />
                </div>
              </div>
              <label className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" checked={filters.in_stock}
                  onChange={e => setFilters(f => ({...f, in_stock: e.target.checked}))}
                  className="w-4 h-4 accent-amber-500" />
                <span className="text-sm text-stone-300">In stock only</span>
              </label>
              <button onClick={() => setFilters({min_price:'',max_price:'',in_stock:false})}
                className="text-xs text-amber-500 hover:text-amber-400">Clear filters</button>
            </aside>
          )}

          <div className="flex-1">
            {loading ? (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {Array.from({length:8}).map((_,i) => (
                  <div key={i} className="animate-pulse">
                    <div className="aspect-[3/4] bg-stone-800 rounded-sm mb-3" />
                    <div className="h-3 bg-stone-800 rounded w-1/2 mb-2" />
                    <div className="h-4 bg-stone-800 rounded w-3/4 mb-2" />
                    <div className="h-3 bg-stone-800 rounded w-1/3" />
                  </div>
                ))}
              </div>
            ) : products.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-24 gap-4">
                <p className="serif text-3xl text-stone-600">No products found</p>
                <button onClick={() => { setSearch(''); setFilters({min_price:'',max_price:'',in_stock:false}) }}
                  className="text-xs uppercase tracking-widest text-amber-500 hover:text-amber-400">Clear filters</button>
              </div>
            ) : (
              <>
                <p className="text-xs text-stone-500 mb-6">{products.length} product{products.length !== 1 ? 's' : ''}</p>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {products.map(p => <ProductCard key={p.id} product={p} />)}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
