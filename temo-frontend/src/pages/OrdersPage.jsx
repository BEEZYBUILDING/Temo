import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ordersApi } from '../api/orders'
import { ShoppingBag, ChevronRight } from 'lucide-react'

const statusColors = {
  PENDING: 'text-yellow-400 bg-yellow-400/10',
  CONFIRMED: 'text-blue-400 bg-blue-400/10',
  PROCESSING: 'text-blue-400 bg-blue-400/10',
  SHIPPED: 'text-purple-400 bg-purple-400/10',
  DELIVERED: 'text-green-400 bg-green-400/10',
  CANCELLED: 'text-red-400 bg-red-400/10',
  REFUNDED: 'text-stone-400 bg-stone-400/10',
}

export default function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    ordersApi.list()
      .then(({ data }) => setOrders(data.results || data))
      .catch(() => setOrders([]))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen pt-20 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen pt-24 max-w-4xl mx-auto px-6 pb-16">
      <h1 className="serif text-4xl font-light text-stone-100 mb-8">Order History</h1>

      {orders.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 gap-4">
          <ShoppingBag size={48} className="text-stone-700" />
          <p className="serif text-2xl text-stone-500">No orders yet</p>
          <Link to="/products" className="text-sm text-amber-500 hover:text-amber-400 uppercase tracking-widest">
            Start Shopping →
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className="block border border-stone-800 hover:border-stone-700 rounded-sm p-5 transition-colors group"
            >
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <div className="flex items-center gap-3">
                    <p className="mono text-sm text-stone-200">#{order.id.slice(0, 8).toUpperCase()}</p>
                    <span className={`px-2 py-0.5 rounded-sm text-[10px] uppercase tracking-widest ${statusColors[order.status] || 'text-stone-400 bg-stone-400/10'}`}>
                      {order.status}
                    </span>
                  </div>
                  <p className="text-xs text-stone-500">
                    {new Date(order.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                  </p>
                  <p className="text-xs text-stone-500">
                    {order.items?.length || 0} item{order.items?.length !== 1 ? 's' : ''}
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <p className="mono text-lg text-amber-400">${parseFloat(order.total).toFixed(2)}</p>
                  <ChevronRight size={16} className="text-stone-600 group-hover:text-stone-300 group-hover:translate-x-1 transition-all" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
