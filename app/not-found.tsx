import { Metadata } from 'next'
import Navbar from '@/components/Navbar'

export const metadata: Metadata = {
  title: '404 - Página não encontrada',
  description: 'Página não encontrada',
}

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <Navbar />
      <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
        <div className="text-center px-4">
          <h1 className="text-6xl font-bold gradient-text mb-4">404</h1>
          <p className="text-2xl text-gray-600 mb-8">Página não encontrada</p>
          <a href="/" className="btn-primary inline-block">
            Voltar para Home
          </a>
        </div>
      </div>
    </div>
  )
}
