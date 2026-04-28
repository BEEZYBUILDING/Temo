import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ShoppingBag, Search, User, Menu, X, LogOut } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { useCartStore } from '../../store/cartStore'
import toast from 'react-hot-toast'

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const { itemCount, setOpen } = useCartStore()
  const [menuOpen, setMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const navigate = useNavigate()

  const handleLogout = async () => {
    const refresh = localStorage.getItem('refresh_token')
    await logout(refresh)
    toast.success('Logged out')
    navigate('/')
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-stone-800 bg-stone-950/95 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <span className="serif text-2xl font-light tracking-widest text-amber-400">TEMO</span>
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mb-1" />
        </Link>

        <div className="hidden md:flex items-center gap-8 text-xs uppercase tracking-widest text-stone-400">
          <Link to="/products" className="hover:text-stone-100 transition-colors">Shop</Link>
          <Link to="/products?category=new" className="hover:text-stone-100 transition-colors">New</Link>
          <Link to="/products?category=sale" className="hover:text-stone-100 transition-colors">Sale</Link>
        </div>

        <div className="flex items-center gap-3">
          <Link to="/products" className="p-2 text-stone-400 hover:text-stone-100 transition-colors">
            <Search size={18} />
          </Link>

          <button
            onClick={() => setOpen(true)}
            className="p-2 text-stone-400 hover:text-stone-100 transition-colors relative"
          >
            <ShoppingBag size={18} />
            {itemCount > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-amber-500 text-stone-950 text-[10px] font-bold rounded-full flex items-center justify-center">
                {itemCount > 9 ? '9+' : itemCount}
              </span>
            )}
          </button>

          {isAuthenticated ? (
            <div className="relative">
              <button
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="p-2 text-stone-400 hover:text-stone-100 transition-colors flex items-center gap-2"
              >
                <User size={18} />
                <span className="hidden md:block text-xs tracking-wider">
                  {user?.first_name || user?.email?.split('@')[0]}
                </span>
              </button>
              {userMenuOpen && (
                <div className="absolute right-0 top-12 w-48 bg-stone-900 border border-stone-800 rounded-sm shadow-2xl">
                  <Link to="/profile" onClick={() => setUserMenuOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 text-sm text-stone-300 hover:text-stone-100 hover:bg-stone-800">
                    <User size={14} /> Profile
                  </Link>
                  <Link to="/orders" onClick={() => setUserMenuOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 text-sm text-stone-300 hover:text-stone-100 hover:bg-stone-800">
                    <ShoppingBag size={14} /> Orders
                  </Link>
                  <hr className="border-stone-800" />
                  <button onClick={() => { setUserMenuOpen(false); handleLogout() }}
                    className="flex items-center gap-3 w-full px-4 py-3 text-sm text-red-400 hover:text-red-300 hover:bg-stone-800">
                    <LogOut size={14} /> Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <Link to="/login"
              className="px-4 py-2 text-xs uppercase tracking-widest text-amber-500 border border-stone-700 hover:border-amber-600 hover:text-amber-400 transition-colors rounded-sm">
              Sign In
            </Link>
          )}

          <button className="md:hidden p-2 text-stone-400" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="md:hidden border-t border-stone-800 bg-stone-950">
          {['Shop', 'New', 'Sale'].map((item) => (
            <Link key={item} to={`/products`} onClick={() => setMenuOpen(false)}
              className="block px-6 py-4 text-sm uppercase tracking-widest text-stone-400 hover:text-stone-100 border-b border-stone-800/50">
              {item}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
