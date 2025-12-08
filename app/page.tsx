import Navbar from '@/components/Navbar'
import { StatsGrid } from '@/components/StatCard'
import { BarChartComponent, LineChartComponent, PieChartComponent } from '@/components/Charts'
import { ArrowRight } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <Navbar />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
            <span className="gradient-text">Plataforma de Saneamento</span>
          </h1>
          <p className="text-gray-600 text-lg md:text-xl max-w-2xl mx-auto mb-8">
            Gerencie seus projetos de saneamento com eficiência, visualize métricas em tempo real e tome decisões baseadas em dados.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="btn-primary flex items-center justify-center gap-2">
              Começar Agora
              <ArrowRight size={20} />
            </button>
            <button className="btn-secondary">Saiba Mais</button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="mb-16">
          <StatsGrid />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          <div className="glass-effect p-8">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Evolução Mensal</h2>
            <BarChartComponent />
          </div>
          <div className="glass-effect p-8">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Tendência</h2>
            <LineChartComponent />
          </div>
        </div>

        {/* Pie Chart Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
          <div className="lg:col-span-1 glass-effect p-8">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Status dos Projetos</h2>
            <PieChartComponent />
          </div>

          {/* Features Section */}
          <div className="lg:col-span-2 glass-effect p-8">
            <h2 className="text-2xl font-bold text-navy-900 mb-8">Funcionalidades Principais</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { icon: '📈', title: 'Análise em Tempo Real', desc: 'Acompanhe suas métricas instantaneamente' },
                { icon: '🔒', title: 'Segurança Garantida', desc: 'Dados protegidos com criptografia de ponta' },
                { icon: '⚡', title: 'Performance', desc: 'Carregamento rápido e resposta imediata' },
                { icon: '🌍', title: 'Escalável', desc: 'Cresce com suas necessidades' },
              ].map((feature, idx) => (
                <div key={idx} className="p-4 bg-gradient-to-br from-navy-50 to-teal-50 rounded-lg">
                  <div className="text-3xl mb-2">{feature.icon}</div>
                  <h3 className="font-bold text-navy-900 mb-2">{feature.title}</h3>
                  <p className="text-sm text-gray-600">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-navy-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-lg mb-4">Saneamento</h3>
              <p className="text-gray-400">Plataforma líder em gestão de projetos de saneamento.</p>
            </div>
            <div>
              <h4 className="font-bold mb-4">Produto</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition">Features</a></li>
                <li><a href="#" className="hover:text-white transition">Preços</a></li>
                <li><a href="#" className="hover:text-white transition">Segurança</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Empresa</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition">Sobre</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Contato</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition">Privacidade</a></li>
                <li><a href="#" className="hover:text-white transition">Termos</a></li>
                <li><a href="#" className="hover:text-white transition">Cookies</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-navy-700 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Saneamento App. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
