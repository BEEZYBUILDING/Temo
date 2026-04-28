import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

import { useAuthStore } from './store/authStore'
import { useCartStore } from './store/cartStore'

import Navbar from './components/layout/Navbar'
import CartDrawer from './components/cart/CartDrawer'
import ProtectedRoute from './components/auth/ProtectedRoute'

import HomePage from './pages/HomePage'
import ProductsPage from './pages/ProductsPage'
import ProductDetailPage from './pages/ProductDetailPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import OrdersPage from './pages/OrdersPage'
import CheckoutPage from './pages/CheckoutPage'

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => { window.scrollTo(0, 0) }, [pathname])
  return null
}

const BARE_ROUTES = ['/login', '/register']

function Layout({ children }) {
  const { pathname } = useLocation()
  const isBare = BARE_ROUTES.includes(pathname)

  return (
    <div className="min-h-screen flex flex-col">
      {!isBare && <Navbar />}
      <main className="flex-1">{children}</main>
      {!isBare && (
        <footer className="border-t border-stone-800 mt-20">
          <div className="max-w-7xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <span className="serif text-xl text-amber-400 tracking-widest">TEMO</span>
              <p className="text-sm text-stone-500 mt-3 max-w-xs">Curated pieces for those who appreciate quiet, considered design.</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-widest text-stone-400 mb-4">Shop</p>
              <div className="space-y-2">
                {[['All Products', '/products'], ['New Arrivals', '/products?category=new']].map(([l,t]) => (
                  <a key={l} href={t} className="block text-sm text-stone-500 hover:text-stone-300">{l}</a>
                ))}
              </div>
            </div>
            <div>
              <p className="text-xs uppercase tracking-widest text-stone-400 mb-4">Account</p>
              <div className="space-y-2">
                {[['Profile', '/profile'], ['Orders', '/orders'], ['Sign In', '/login']].map(([l,t]) => (
                  <a key={l} href={t} className="block text-sm text-stone-500 hover:text-stone-300">{l}</a>
                ))}
              </div>
            </div>
          </div>
          <div className="border-t border-stone-800/50 py-6 text-center">
            <p className="text-xs text-stone-700">© {new Date().getFullYear()} Temo. All rights reserved.</p>
          </div>
        </footer>
      )}
      <CartDrawer />
    </div>
  )
}

function AppRoutes() {
  const { initialize } = useAuthStore()
  const { fetchCart } = useCartStore()

  useEffect(() => {
    initialize()
    fetchCart()
  }, [])

  return (
    <Layout>
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/checkout" element={<ProtectedRoute><CheckoutPage /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        <Route path="/orders" element={<ProtectedRoute><OrdersPage /></ProtectedRoute>} />
        <Route path="*" element={
          <div className="min-h-screen flex flex-col items-center justify-center gap-4">
            <p className="serif text-6xl text-stone-700">404</p>
            <p className="text-stone-500">Page not found</p>
            <a href="/" className="text-amber-500 text-sm hover:text-amber-400">← Go home</a>
          </div>
        } />
      </Routes>
    </Layout>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="bottom-right" toastOptions={{
        style: { background: '#1c1916', color: '#f0ebe3', border: '1px solid #2a2520', fontFamily: "'DM Sans', sans-serif", fontSize: '14px' },
        success: { iconTheme: { primary: '#c8922a', secondary: '#0c0b09' } },
        error: { iconTheme: { primary: '#c0392b', secondary: '#0c0b09' } },
      }} />
      <AppRoutes />
    </BrowserRouter>
  )
}
