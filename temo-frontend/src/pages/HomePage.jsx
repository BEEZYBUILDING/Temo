import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <section className="relative h-screen flex items-center overflow-hidden">
        <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage:'linear-gradient(#2a2520 1px,transparent 1px),linear-gradient(90deg,#2a2520 1px,transparent 1px)',backgroundSize:'80px 80px'}} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-amber-600/5 rounded-full blur-[120px] pointer-events-none" />
        <div className="max-w-7xl mx-auto px-6 pt-20 w-full">
          <div className="max-w-3xl">
            <p className="text-xs uppercase tracking-[0.3em] text-amber-500 mb-6 mono">— New Season</p>
            <h1 className="serif text-7xl md:text-9xl font-light leading-none text-stone-100 mb-8">
              Curated<br /><span className="italic text-amber-400">elegance</span>
            </h1>
            <p className="text-stone-400 text-lg font-light max-w-md mb-12 leading-relaxed">
              Discover pieces crafted for those who appreciate the quiet luxury of considered design.
            </p>
            <div className="flex items-center gap-6">
              <Link to="/products" className="group flex items-center gap-3 px-8 py-4 bg-amber-500 text-stone-950 text-sm uppercase tracking-widest font-medium hover:bg-amber-400 transition-colors rounded-sm">
                Shop Now <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link to="/products" className="text-sm uppercase tracking-widest text-stone-400 hover:text-stone-100 transition-colors">
                New Arrivals →
              </Link>
            </div>
          </div>
        </div>
        <div className="absolute bottom-12 right-12 hidden lg:flex flex-col items-end gap-2">
          <span className="w-16 h-px bg-amber-600/40" />
          <p className="text-[10px] tracking-[0.3em] text-stone-600 uppercase">Est. 2024</p>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="flex items-center gap-4 mb-12">
          <span className="w-8 h-px bg-amber-600" />
          <h2 className="serif text-3xl font-light text-stone-200">Collections</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[{name:'New Arrivals',desc:'Just in'},{name:'Accessories',desc:'Finish the look'},{name:'Clothing',desc:'Essentials & more'}].map((cat,i) => (
            <Link key={i} to="/products" className="group relative aspect-[4/5] bg-stone-900 rounded-sm overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/20 to-transparent" />
              <div className="absolute bottom-0 left-0 right-0 p-6">
                <p className="text-xs text-stone-500 uppercase tracking-widest mb-1">{cat.desc}</p>
                <h3 className="serif text-2xl text-stone-100 group-hover:text-amber-400 transition-colors">{cat.name}</h3>
                <span className="inline-flex items-center gap-2 text-xs uppercase tracking-widest text-amber-500 mt-3 group-hover:gap-3 transition-all">
                  Explore <ArrowRight size={12} />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="border-t border-stone-800/50">
        <div className="max-w-7xl mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          {[{title:'Free Shipping',desc:'On all orders over $150'},{title:'Easy Returns',desc:'30-day return policy'},{title:'Secure Payment',desc:'Your data is protected'}].map(f => (
            <div key={f.title} className="text-center space-y-2">
              <h4 className="serif text-xl text-stone-200">{f.title}</h4>
              <p className="text-sm text-stone-500">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
